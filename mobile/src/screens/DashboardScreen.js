import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
  Dimensions,
  Platform
} from 'react-native';
import { Card, Title, Paragraph, Button, FAB, Portal, Modal, TextInput, Chip } from 'react-native-paper';
import { LineChart, BarChart, PieChart } from 'react-native-chart-kit';
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';
import PushNotification from 'react-native-push-notification';

const screenWidth = Dimensions.get('window').width;

const DashboardScreen = ({ navigation, user }) => {
  const [dashboardData, setDashboardData] = useState({
    projects: [],
    kpis: [],
    risks: [],
    notifications: []
  });
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(true);
  const [lastSync, setLastSync] = useState(null);
  const [pendingActions, setPendingActions] = useState([]);
  const [showQuickActions, setShowQuickActions] = useState(false);

  // Configurar notificaciones push
  useEffect(() => {
    configurePushNotifications();
    setupNetworkListener();
    loadCachedData();
    fetchDashboardData();
    
    // Sincronización automática cada 30 segundos
    const syncInterval = setInterval(() => {
      if (isConnected) {
        syncPendingActions();
        fetchDashboardData();
      }
    }, 30000);

    return () => clearInterval(syncInterval);
  }, []);

  const configurePushNotifications = () => {
    PushNotification.configure({
      onRegister: function (token) {
        console.log('TOKEN:', token);
        // Enviar token al servidor
        registerDeviceToken(token.token);
      },
      onNotification: function (notification) {
        console.log('NOTIFICATION:', notification);
        if (notification.userInteraction) {
          // Usuario tocó la notificación
          handleNotificationTap(notification);
        }
      },
      permissions: {
        alert: true,
        badge: true,
        sound: true,
      },
      popInitialNotification: true,
      requestPermissions: Platform.OS === 'ios',
    });
  };

  const setupNetworkListener = () => {
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsConnected(state.isConnected);
      if (state.isConnected && pendingActions.length > 0) {
        syncPendingActions();
      }
    });
    return unsubscribe;
  };

  const loadCachedData = async () => {
    try {
      const cachedData = await AsyncStorage.getItem('dashboardData');
      const cachedSync = await AsyncStorage.getItem('lastSync');
      const cachedPending = await AsyncStorage.getItem('pendingActions');
      
      if (cachedData) {
        setDashboardData(JSON.parse(cachedData));
      }
      if (cachedSync) {
        setLastSync(new Date(cachedSync));
      }
      if (cachedPending) {
        setPendingActions(JSON.parse(cachedPending));
      }
    } catch (error) {
      console.error('Error loading cached data:', error);
    }
  };

  const fetchDashboardData = async () => {
    if (!isConnected) return;
    
    setIsLoading(true);
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/dashboard/mobile', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
        setLastSync(new Date());
        
        // Cachear datos
        await AsyncStorage.setItem('dashboardData', JSON.stringify(data));
        await AsyncStorage.setItem('lastSync', new Date().toISOString());
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      Alert.alert('Error', 'No se pudieron cargar los datos del dashboard');
    } finally {
      setIsLoading(false);
    }
  };

  const syncPendingActions = async () => {
    if (pendingActions.length === 0) return;

    try {
      const token = await AsyncStorage.getItem('token');
      
      for (const action of pendingActions) {
        const response = await fetch(action.url, {
          method: action.method,
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(action.data)
        });

        if (response.ok) {
          // Remover acción sincronizada
          setPendingActions(prev => prev.filter(a => a.id !== action.id));
        }
      }

      // Actualizar cache
      await AsyncStorage.setItem('pendingActions', JSON.stringify(pendingActions));
    } catch (error) {
      console.error('Error syncing pending actions:', error);
    }
  };

  const addPendingAction = async (action) => {
    const newAction = {
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
      ...action
    };
    
    const updatedActions = [...pendingActions, newAction];
    setPendingActions(updatedActions);
    await AsyncStorage.setItem('pendingActions', JSON.stringify(updatedActions));
  };

  const registerDeviceToken = async (token) => {
    try {
      const authToken = await AsyncStorage.getItem('token');
      await fetch('http://localhost:5000/api/notifications/register-device', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          device_token: token,
          platform: Platform.OS
        })
      });
    } catch (error) {
      console.error('Error registering device token:', error);
    }
  };

  const handleNotificationTap = (notification) => {
    if (notification.data?.projectId) {
      navigation.navigate('ProjectDetail', { projectId: notification.data.projectId });
    } else if (notification.data?.screen) {
      navigation.navigate(notification.data.screen);
    }
  };

  const quickUpdateProject = async (projectId, field, value) => {
    const action = {
      url: `http://localhost:5000/api/projects/${projectId}`,
      method: 'PUT',
      data: { [field]: value }
    };

    if (isConnected) {
      try {
        const token = await AsyncStorage.getItem('token');
        const response = await fetch(action.url, {
          method: action.method,
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(action.data)
        });

        if (response.ok) {
          fetchDashboardData(); // Refrescar datos
          Alert.alert('Éxito', 'Proyecto actualizado correctamente');
        }
      } catch (error) {
        await addPendingAction(action);
        Alert.alert('Sin conexión', 'La actualización se sincronizará cuando tengas conexión');
      }
    } else {
      await addPendingAction(action);
      Alert.alert('Sin conexión', 'La actualización se sincronizará cuando tengas conexión');
    }
  };

  const chartConfig = {
    backgroundGradientFrom: '#ffffff',
    backgroundGradientTo: '#ffffff',
    color: (opacity = 1) => `rgba(0, 122, 255, ${opacity})`,
    strokeWidth: 2,
    barPercentage: 0.5,
    useShadowColorFromDataset: false,
  };

  const projectStatusData = [
    {
      name: 'Activos',
      population: dashboardData.projects?.filter(p => p.estado === 'activo').length || 0,
      color: '#00C49F',
      legendFontColor: '#7F7F7F',
      legendFontSize: 15,
    },
    {
      name: 'Completados',
      population: dashboardData.projects?.filter(p => p.estado === 'completado').length || 0,
      color: '#0088FE',
      legendFontColor: '#7F7F7F',
      legendFontSize: 15,
    },
    {
      name: 'En Pausa',
      population: dashboardData.projects?.filter(p => p.estado === 'pausado').length || 0,
      color: '#FFBB28',
      legendFontColor: '#7F7F7F',
      legendFontSize: 15,
    },
  ];

  return (
    <View style={styles.container}>
      <ScrollView
        refreshControl={
          <RefreshControl refreshing={isLoading} onRefresh={fetchDashboardData} />
        }
      >
        {/* Header con estado de conexión */}
        <View style={styles.header}>
          <Title>Dashboard</Title>
          <View style={styles.statusContainer}>
            <Chip 
              icon={isConnected ? 'wifi' : 'wifi-off'} 
              mode="outlined"
              compact
              style={[styles.statusChip, { backgroundColor: isConnected ? '#e8f5e8' : '#ffeaea' }]}
            >
              {isConnected ? 'En línea' : 'Sin conexión'}
            </Chip>
            {pendingActions.length > 0 && (
              <Chip icon="sync" mode="outlined" compact style={styles.pendingChip}>
                {pendingActions.length} pendientes
              </Chip>
            )}
          </View>
        </View>

        {/* Métricas principales */}
        <View style={styles.metricsContainer}>
          <Card style={styles.metricCard}>
            <Card.Content>
              <Title>{dashboardData.projects?.length || 0}</Title>
              <Paragraph>Proyectos Totales</Paragraph>
            </Card.Content>
          </Card>
          
          <Card style={styles.metricCard}>
            <Card.Content>
              <Title>{dashboardData.projects?.filter(p => p.estado === 'activo').length || 0}</Title>
              <Paragraph>Proyectos Activos</Paragraph>
            </Card.Content>
          </Card>
        </View>

        {/* Gráfico de estado de proyectos */}
        <Card style={styles.chartCard}>
          <Card.Content>
            <Title>Estado de Proyectos</Title>
            <PieChart
              data={projectStatusData}
              width={screenWidth - 60}
              height={220}
              chartConfig={chartConfig}
              accessor="population"
              backgroundColor="transparent"
              paddingLeft="15"
              absolute
            />
          </Card.Content>
        </Card>

        {/* Lista de proyectos recientes */}
        <Card style={styles.projectsCard}>
          <Card.Content>
            <Title>Proyectos Recientes</Title>
            {dashboardData.projects?.slice(0, 5).map((project, index) => (
              <TouchableOpacity
                key={project.id}
                style={styles.projectItem}
                onPress={() => navigation.navigate('ProjectDetail', { projectId: project.id })}
              >
                <View style={styles.projectInfo}>
                  <Text style={styles.projectName}>{project.nombre}</Text>
                  <Text style={styles.projectStatus}>{project.estado}</Text>
                </View>
                <Text style={styles.projectProgress}>{project.progreso_general}%</Text>
              </TouchableOpacity>
            ))}
          </Card.Content>
        </Card>

        {/* Información de sincronización */}
        {lastSync && (
          <View style={styles.syncInfo}>
            <Text style={styles.syncText}>
              Última sincronización: {lastSync.toLocaleTimeString()}
            </Text>
          </View>
        )}
      </ScrollView>

      {/* FAB para acciones rápidas */}
      <Portal>
        <FAB.Group
          open={showQuickActions}
          icon={showQuickActions ? 'close' : 'plus'}
          actions={[
            {
              icon: 'folder-plus',
              label: 'Nuevo Proyecto',
              onPress: () => navigation.navigate('CreateProject'),
            },
            {
              icon: 'sync',
              label: 'Sincronizar',
              onPress: () => {
                syncPendingActions();
                fetchDashboardData();
              },
            },
            {
              icon: 'bell',
              label: 'Notificaciones',
              onPress: () => navigation.navigate('Notifications'),
            },
          ]}
          onStateChange={({ open }) => setShowQuickActions(open)}
        />
      </Portal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
    elevation: 2,
  },
  statusContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  statusChip: {
    height: 32,
  },
  pendingChip: {
    height: 32,
    backgroundColor: '#fff3cd',
  },
  metricsContainer: {
    flexDirection: 'row',
    padding: 16,
    gap: 16,
  },
  metricCard: {
    flex: 1,
    elevation: 2,
  },
  chartCard: {
    margin: 16,
    elevation: 2,
  },
  projectsCard: {
    margin: 16,
    elevation: 2,
  },
  projectItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  projectInfo: {
    flex: 1,
  },
  projectName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  projectStatus: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  projectProgress: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#007AFF',
  },
  syncInfo: {
    padding: 16,
    alignItems: 'center',
  },
  syncText: {
    fontSize: 12,
    color: '#666',
  },
});

export default DashboardScreen;

