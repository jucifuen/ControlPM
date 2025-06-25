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
import PortfolioDashboard from './PortfolioDashboard'

const Dashboard = ({ user, token, onLogout }) => {
  const [projects, setProjects] = useState([])
  const [selectedProject, setSelectedProject] = useState(null)
  const [showProjectForm, setShowProjectForm] = useState(false)
  const [activeTab, setActiveTab] = useState('resumen')

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
      if (response.ok) {
        const data = await response.json()
        setProjects(data)
      }
    } catch (error) {
      console.error('Error fetching projects:', error)
    }
  }

  const handleProjectCreated = (newProject) => {
    setProjects([...projects, newProject])
    setShowProjectForm(false)
  }

  const handleProjectSelect = (project) => {
    setSelectedProject(project)
    setActiveTab('resumen')
  }

  if (showProjectForm) {
    return (
      <ProjectForm
        token={token}
        onProjectCreated={handleProjectCreated}
        onCancel={() => setShowProjectForm(false)}
      />
    )
  }

  if (selectedProject) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between h-16">
              <div className="flex items-center space-x-4">
                <Button
                  variant="ghost"
                  onClick={() => setSelectedProject(null)}
                  className="flex items-center space-x-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  <span>Volver a proyectos</span>
                </Button>
                <div>
                  <h1 className="text-xl font-semibold text-gray-900">{selectedProject.nombre}</h1>
                  <p className="text-sm text-gray-500">{selectedProject.descripcion}</p>
                </div>
              </div>
              <Button
                variant="outline"
                className="flex items-center space-x-2"
              >
                <Settings className="h-4 w-4" />
                <span>Configurar</span>
              </Button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="resumen">Resumen</TabsTrigger>
              <TabsTrigger value="kpis">KPIs</TabsTrigger>
              <TabsTrigger value="riesgos">Riesgos</TabsTrigger>
              <TabsTrigger value="recursos">Recursos</TabsTrigger>
              <TabsTrigger value="fases">Fases</TabsTrigger>
            </TabsList>

            <TabsContent value="resumen" className="space-y-6">
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
              <div className="text-center py-12">
                <BarChart3 className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">KPIs del Proyecto</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Indicadores clave de rendimiento para monitorear el progreso del proyecto.
                </p>
              </div>
            </TabsContent>

            <TabsContent value="riesgos">
              <div className="text-center py-12">
                <AlertTriangle className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Gestión de Riesgos</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Funcionalidad en desarrollo...
                </p>
              </div>
            </TabsContent>

            <TabsContent value="recursos">
              <div className="text-center py-12">
                <Users className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Gestión de Recursos</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Funcionalidad en desarrollo...
                </p>
              </div>
            </TabsContent>

            <TabsContent value="fases">
              <div className="text-center py-12">
                <Calendar className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Fases del Proyecto</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Gestión de fases y cronograma del proyecto.
                </p>
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <h1 className="text-2xl font-bold text-blue-600">Avanzando</h1>
              <Badge variant="secondary">{user.rol}</Badge>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">Hola, {user.nombre}</span>
              <Button
                variant="outline"
                onClick={onLogout}
                className="flex items-center space-x-2"
              >
                <LogOut className="h-4 w-4" />
                <span>Salir</span>
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs defaultValue="proyectos" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="proyectos">Mis Proyectos</TabsTrigger>
            <TabsTrigger value="portfolio">Dashboard Portafolio</TabsTrigger>
          </TabsList>

          <TabsContent value="proyectos" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Proyectos</CardTitle>
                  <FolderOpen className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{projects.length}</div>
                  <p className="text-xs text-muted-foreground">
                    {projects.filter(p => p.estado === 'activo').length} activos
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Proyectos Activos</CardTitle>
                  <BarChart3 className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {projects.filter(p => p.estado === 'activo').length}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    En progreso
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Completados</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    {projects.filter(p => p.estado === 'completado').length}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Finalizados
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Presupuesto Total</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">
                    ${projects.reduce((sum, p) => sum + (p.presupuesto_estimado || 0), 0).toLocaleString()}
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Estimado total
                  </p>
                </CardContent>
              </Card>
            </div>

            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">Proyectos</h2>
              <Button
                onClick={() => setShowProjectForm(true)}
                className="flex items-center space-x-2"
              >
                <Plus className="h-4 w-4" />
                <span>Nuevo Proyecto</span>
              </Button>
            </div>

            {projects.length === 0 ? (
              <Card>
                <CardContent className="flex flex-col items-center justify-center py-12">
                  <FolderOpen className="h-12 w-12 text-gray-400 mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No hay proyectos</h3>
                  <p className="text-gray-500 text-center mb-6">
                    Comience creando su primer proyecto.
                  </p>
                  <Button
                    onClick={() => setShowProjectForm(true)}
                    className="flex items-center space-x-2"
                  >
                    <Plus className="h-4 w-4" />
                    <span>Crear Primer Proyecto</span>
                  </Button>
                </CardContent>
              </Card>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project) => (
                  <Card 
                    key={project.id} 
                    className="cursor-pointer hover:shadow-lg transition-shadow"
                    onClick={() => handleProjectSelect(project)}
                  >
                    <CardHeader>
                      <div className="flex items-center justify-between">
                        <CardTitle className="text-lg">{project.nombre}</CardTitle>
                        <Badge variant={project.estado === 'activo' ? 'default' : 'secondary'}>
                          {project.estado}
                        </Badge>
                      </div>
                      <CardDescription>{project.descripcion}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span>Presupuesto:</span>
                          <span className="font-medium">
                            ${project.presupuesto_estimado?.toLocaleString() || '0'}
                          </span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span>Inicio:</span>
                          <span>{new Date(project.fecha_inicio).toLocaleDateString()}</span>
                        </div>
                        {project.fecha_fin_estimada && (
                          <div className="flex justify-between text-sm">
                            <span>Fin estimado:</span>
                            <span>{new Date(project.fecha_fin_estimada).toLocaleDateString()}</span>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="portfolio">
            <PortfolioDashboard user={user} />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default Dashboard

