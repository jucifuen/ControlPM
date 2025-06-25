import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Dimensions
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

const { width } = Dimensions.get('window');

export default function DashboardScreen() {
  const [dashboardData, setDashboardData] = useState({
    totalProjects: 0,
    activeProjects: 0,
    completedProjects: 0,
    totalBudget: 0,
    recentProjects: []
  });
  const [refreshing, setRefreshing] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    loadUserData();
    fetchDashboardData();
  }, []);

  const loadUserData = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        setUser(JSON.parse(userData));
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const fetchDashboardData = async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/portfolio', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData({
          totalProjects: data.totalProjects,
          activeProjects: data.activeProjects,
          completedProjects: data.completedProjects,
          totalBudget: data.totalBudget,
          recentProjects: data.projects.slice(0, 5)
        });
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchDashboardData();
    setRefreshing(false);
  };

  const MetricCard = ({ title, value, icon, color = '#3B82F6' }) => (
    <View style={[styles.metricCard, { borderLeftColor: color }]}>
      <View style={styles.metricHeader}>
        <Ionicons name={icon} size={24} color={color} />
        <Text style={styles.metricTitle}>{title}</Text>
      </View>
      <Text style={styles.metricValue}>{value}</Text>
    </View>
  );

  const ProjectCard = ({ project }) => (
    <TouchableOpacity style={styles.projectCard}>
      <View style={styles.projectHeader}>
        <Text style={styles.projectName}>{project.nombre}</Text>
        <View style={[styles.statusBadge, { 
          backgroundColor: project.estado === 'activo' ? '#10B981' : '#6B7280' 
        }]}>
          <Text style={styles.statusText}>{project.estado}</Text>
        </View>
      </View>
      <Text style={styles.projectDescription} numberOfLines={2}>
        {project.descripcion}
      </Text>
      <View style={styles.projectFooter}>
        <Text style={styles.projectBudget}>
          ${project.presupuesto_estimado?.toLocaleString()}
        </Text>
        <Text style={styles.projectProgress}>
          {project.progreso?.toFixed(0)}% completado
        </Text>
      </View>
    </TouchableOpacity>
  );

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Text style={styles.greeting}>
          Hola, {user?.nombre || 'Usuario'}
        </Text>
        <Text style={styles.subtitle}>
          Bienvenido a tu dashboard
        </Text>
      </View>

      <View style={styles.metricsContainer}>
        <MetricCard
          title="Total Proyectos"
          value={dashboardData.totalProjects}
          icon="folder-outline"
          color="#3B82F6"
        />
        <MetricCard
          title="Proyectos Activos"
          value={dashboardData.activeProjects}
          icon="play-circle-outline"
          color="#10B981"
        />
        <MetricCard
          title="Completados"
          value={dashboardData.completedProjects}
          icon="checkmark-circle-outline"
          color="#8B5CF6"
        />
        <MetricCard
          title="Presupuesto Total"
          value={`$${dashboardData.totalBudget?.toLocaleString()}`}
          icon="cash-outline"
          color="#F59E0B"
        />
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Proyectos Recientes</Text>
        {dashboardData.recentProjects.map((project) => (
          <ProjectCard key={project.id} project={project} />
        ))}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  header: {
    padding: 20,
    backgroundColor: 'white',
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  greeting: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1e293b',
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    marginTop: 4,
  },
  metricsContainer: {
    padding: 16,
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  metricCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    width: (width - 48) / 2,
    marginBottom: 16,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  metricHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  metricTitle: {
    fontSize: 14,
    color: '#64748b',
    marginLeft: 8,
    flex: 1,
  },
  metricValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1e293b',
  },
  section: {
    padding: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: 16,
  },
  projectCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  projectHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  projectName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
    flex: 1,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '500',
  },
  projectDescription: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 12,
  },
  projectFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  projectBudget: {
    fontSize: 14,
    fontWeight: '600',
    color: '#059669',
  },
  projectProgress: {
    fontSize: 12,
    color: '#64748b',
  },
});

