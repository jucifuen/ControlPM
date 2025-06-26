import { useState, useEffect } from 'react'
import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Input } from '@/components/ui/input'
import { DatePickerWithRange } from '@/components/ui/date-range-picker'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts'
import { FolderOpen, TrendingUp, AlertTriangle, Users, DollarSign, Calendar, Target, Filter, Download, RefreshCw } from 'lucide-react'

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export default function PortfolioDashboard({ user }) {
  const [portfolioData, setPortfolioData] = useState({
    totalProjects: 0,
    activeProjects: 0,
    completedProjects: 0,
    totalBudget: 0,
    totalSpent: 0,
    projects: [],
    kpiSummary: [],
    riskSummary: [],
    resourceUtilization: []
  })

  // Estados para filtros
  const [filters, setFilters] = useState({
    status: 'all',
    client: 'all',
    dateRange: null,
    searchTerm: '',
    budgetRange: 'all'
  })

  const [isLoading, setIsLoading] = useState(false)
  const [viewMode, setViewMode] = useState('grid') // 'grid' o 'table'

  useEffect(() => {
    fetchPortfolioData()
  }, [filters])

  const fetchPortfolioData = async () => {
    setIsLoading(true)
    try {
      const queryParams = new URLSearchParams()
      if (filters.status !== 'all') queryParams.append('status', filters.status)
      if (filters.client !== 'all') queryParams.append('client', filters.client)
      if (filters.searchTerm) queryParams.append('search', filters.searchTerm)
      if (filters.budgetRange !== 'all') queryParams.append('budget', filters.budgetRange)
      
      const response = await fetch(`http://localhost:5000/api/portfolio?${queryParams}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setPortfolioData(data)
      }
    } catch (error) {
      console.error('Error fetching portfolio data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const exportData = async (format) => {
    try {
      const response = await fetch(`http://localhost:5000/api/portfolio/export?format=${format}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `portfolio-report.${format}`
        a.click()
      }
    } catch (error) {
      console.error('Error exporting data:', error)
    }
  }

  const projectStatusData = [
    { name: 'Activos', value: portfolioData.activeProjects, color: '#00C49F' },
    { name: 'Completados', value: portfolioData.completedProjects, color: '#0088FE' },
    { name: 'En Pausa', value: portfolioData.totalProjects - portfolioData.activeProjects - portfolioData.completedProjects, color: '#FFBB28' }
  ]

  const budgetData = [
    { name: 'Presupuestado', amount: portfolioData.totalBudget },
    { name: 'Gastado', amount: portfolioData.totalSpent },
    { name: 'Disponible', amount: portfolioData.totalBudget - portfolioData.totalSpent }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard de Portafolio</h1>
          <p className="text-muted-foreground">Vista consolidada de todos los proyectos</p>
        </div>
      </div>

      {/* Métricas principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Proyectos</CardTitle>
            <FolderOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{portfolioData.totalProjects}</div>
            <p className="text-xs text-muted-foreground">
              {portfolioData.activeProjects} activos
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Presupuesto Total</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${portfolioData.totalBudget?.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              ${portfolioData.totalSpent?.toLocaleString()} gastado
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Eficiencia</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {portfolioData.totalBudget > 0 ? 
                Math.round((portfolioData.totalSpent / portfolioData.totalBudget) * 100) : 0}%
            </div>
            <p className="text-xs text-muted-foreground">
              Utilización presupuestaria
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Riesgos Activos</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{portfolioData.riskSummary?.length || 0}</div>
            <p className="text-xs text-muted-foreground">
              Requieren atención
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Estado de Proyectos</CardTitle>
            <CardDescription>Distribución por estado</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={projectStatusData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {projectStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Presupuesto vs Gasto</CardTitle>
            <CardDescription>Análisis financiero del portafolio</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={budgetData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                <Bar dataKey="amount" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Lista de proyectos */}
      <Card>
        <CardHeader>
          <CardTitle>Proyectos Activos</CardTitle>
          <CardDescription>Estado actual de todos los proyectos</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {portfolioData.projects?.map((project) => (
              <div key={project.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="space-y-1">
                  <h4 className="font-semibold">{project.nombre}</h4>
                  <p className="text-sm text-muted-foreground">{project.descripcion}</p>
                  <div className="flex items-center space-x-2">
                    <Badge variant={project.estado === 'activo' ? 'default' : 'secondary'}>
                      {project.estado}
                    </Badge>
                    <span className="text-sm text-muted-foreground">
                      Cliente: {project.cliente_nombre}
                    </span>
                  </div>
                </div>
                <div className="text-right space-y-1">
                  <div className="font-semibold">${project.presupuesto_estimado?.toLocaleString()}</div>
                  <Progress 
                    value={project.progreso || 0} 
                    className="w-32"
                  />
                  <div className="text-xs text-muted-foreground">
                    {project.progreso || 0}% completado
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

