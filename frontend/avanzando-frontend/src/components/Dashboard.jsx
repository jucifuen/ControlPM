import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  LogOut, 
  Plus, 
  FolderOpen, 
  DollarSign, 
  Users, 
  Calendar,
  BarChart3,
  AlertTriangle,
  Settings,
  Target,
  ArrowLeft
} from 'lucide-react'
import ProjectForm from './ProjectForm'
import KPIsDashboard from './KPIsDashboard'

const Dashboard = ({ user, token, onLogout }) => {
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)
  const [showProjectForm, setShowProjectForm] = useState(false)
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/projects', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      const data = await response.json()

      if (response.ok) {
        setProjects(data.proyectos || [])
      } else {
        setError(data.error || 'Error al cargar proyectos')
      }
    } catch (err) {
      setError('Error de conexión')
    } finally {
      setLoading(false)
    }
  }

  const handleProjectCreated = (newProject) => {
    setProjects([...projects, newProject])
    setShowProjectForm(false)
    setSelectedProject(newProject)
    setActiveTab('overview')
  }

  const handleProjectSelect = (project) => {
    setSelectedProject(project)
    setActiveTab('overview')
  }

  const getProjectStats = () => {
    const total = projects.length
    const activos = projects.filter(p => p.estado === 'activo').length
    const completados = projects.filter(p => p.estado === 'completado').length
    const presupuestoTotal = projects.reduce((sum, p) => sum + (p.presupuesto_estimado || 0), 0)
    
    return { total, activos, completados, presupuestoTotal }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'activo':
        return 'bg-green-100 text-green-800'
      case 'pausado':
        return 'bg-yellow-100 text-yellow-800'
      case 'completado':
        return 'bg-blue-100 text-blue-800'
      case 'cancelado':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const stats = getProjectStats()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-blue-600">Avanzando</h1>
              <Badge variant="secondary">{user.rol}</Badge>
              {selectedProject && (
                <>
                  <span className="text-gray-300">|</span>
                  <span className="font-medium">{selectedProject.nombre}</span>
                </>
              )}
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Hola, {user.nombre}</span>
              <Button variant="outline" onClick={onLogout}>
                <LogOut className="h-4 w-4 mr-2" />
                Salir
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {!selectedProject ? (
          // Vista principal - Lista de proyectos
          <div className="space-y-6">
            {/* Estadísticas generales */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Proyectos</CardTitle>
                  <FolderOpen className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.total}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Proyectos Activos</CardTitle>
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.activos}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Completados</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats.completados}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Presupuesto Total</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${stats.presupuestoTotal.toLocaleString()}</div>
                </CardContent>
              </Card>
            </div>

            {/* Proyectos */}
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Proyectos</h2>
              <Button onClick={() => setShowProjectForm(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Nuevo Proyecto
              </Button>
            </div>

            {projects.length === 0 ? (
              <Card className="text-center py-12">
                <CardContent>
                  <FolderOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No hay proyectos</h3>
                  <p className="text-gray-600 mb-4">Comience creando su primer proyecto.</p>
                  <Button onClick={() => setShowProjectForm(true)}>
                    <Plus className="h-4 w-4 mr-2" />
                    Crear Primer Proyecto
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project) => (
                  <Card 
                    key={project.id} 
                    className="hover:shadow-lg transition-shadow cursor-pointer"
                    onClick={() => handleProjectSelect(project)}
                  >
                    <CardHeader>
                      <div className="flex justify-between items-start">
                        <div>
                          <CardTitle className="text-lg">{project.nombre}</CardTitle>
                          <CardDescription>{project.descripcion}</CardDescription>
                        </div>
                        <Badge className={getStatusColor(project.estado)}>
                          {project.estado}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Cliente:</span>
                          <span className="font-medium">{project.cliente_nombre}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span>Presupuesto:</span>
                          <span className="font-medium">
                            ${(project.presupuesto_estimado || 0).toLocaleString()}
                          </span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span>Inicio:</span>
                          <span>{project.fecha_inicio ? new Date(project.fecha_inicio).toLocaleDateString() : 'No definida'}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </div>
        ) : (
          // Vista detallada del proyecto
          <div className="space-y-6">
            {/* Header del proyecto */}
            <div className="flex justify-between items-center">
              <div>
                <Button 
                  variant="ghost" 
                  onClick={() => setSelectedProject(null)}
                  className="mb-2"
                >
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Volver a proyectos
                </Button>
                <h1 className="text-2xl font-bold">{selectedProject.nombre}</h1>
                <p className="text-gray-600">{selectedProject.descripcion}</p>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline">
                  <Settings className="h-4 w-4 mr-2" />
                  Configurar
                </Button>
              </div>
            </div>

            {/* Tabs del proyecto */}
            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-5">
                <TabsTrigger value="overview">Resumen</TabsTrigger>
                <TabsTrigger value="kpis">KPIs</TabsTrigger>
                <TabsTrigger value="riesgos">Riesgos</TabsTrigger>
                <TabsTrigger value="recursos">Recursos</TabsTrigger>
                <TabsTrigger value="fases">Fases</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <Target className="h-5 w-5 mr-2" />
                        KPIs
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-2xl font-bold">0</p>
                      <p className="text-sm text-gray-600">Indicadores definidos</p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <AlertTriangle className="h-5 w-5 mr-2" />
                        Riesgos
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-2xl font-bold">0</p>
                      <p className="text-sm text-gray-600">Riesgos identificados</p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <Users className="h-5 w-5 mr-2" />
                        Recursos
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-2xl font-bold">0</p>
                      <p className="text-sm text-gray-600">Recursos asignados</p>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              <TabsContent value="kpis">
                <KPIsDashboard proyecto={selectedProject} token={token} />
              </TabsContent>

              <TabsContent value="riesgos">
                <div className="text-center py-12">
                  <AlertTriangle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Gestión de Riesgos</h3>
                  <p className="text-gray-600">Funcionalidad en desarrollo...</p>
                </div>
              </TabsContent>

              <TabsContent value="recursos">
                <div className="text-center py-12">
                  <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Gestión de Recursos</h3>
                  <p className="text-gray-600">Funcionalidad en desarrollo...</p>
                </div>
              </TabsContent>

              <TabsContent value="fases">
                <div className="text-center py-12">
                  <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Fases del Proyecto</h3>
                  <p className="text-gray-600">Funcionalidad en desarrollo...</p>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        )}
      </div>

      {/* Modal de formulario de proyecto */}
      {showProjectForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <ProjectForm 
              onProjectCreated={handleProjectCreated}
              onCancel={() => setShowProjectForm(false)}
              token={token}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard

