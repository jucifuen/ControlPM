import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown, 
  AlertCircle,
  Plus,
  Edit,
  Trash2,
  Target
} from 'lucide-react'

const KPIsDashboard = ({ proyecto, token }) => {
  const [kpis, setKpis] = useState([])
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (proyecto?.id) {
      fetchKPIs()
      fetchDashboard()
    }
  }, [proyecto])

  const fetchKPIs = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/kpis?proyecto_id=${proyecto.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setKpis(data)
      } else {
        setError('Error al cargar KPIs')
      }
    } catch (err) {
      setError('Error de conexión')
    }
  }

  const fetchDashboard = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/kpis/dashboard/${proyecto.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setDashboard(data)
      }
    } catch (err) {
      console.error('Error al cargar dashboard de KPIs:', err)
    } finally {
      setLoading(false)
    }
  }

  const getEstadoColor = (estado) => {
    const colores = {
      'verde': 'bg-green-500',
      'amarillo': 'bg-yellow-500',
      'rojo': 'bg-red-500'
    }
    return colores[estado] || 'bg-gray-500'
  }

  const getEstadoTexto = (estado) => {
    const textos = {
      'verde': 'Óptimo',
      'amarillo': 'Atención',
      'rojo': 'Crítico'
    }
    return textos[estado] || estado
  }

  const getTipoIcon = (tipo) => {
    const iconos = {
      'tiempo': '⏱️',
      'alcance': '🎯',
      'costo': '💰',
      'calidad': '⭐',
      'recursos': '👥'
    }
    return iconos[tipo] || '📊'
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold">KPIs del Proyecto</h2>
          <p className="text-gray-600">Indicadores clave de rendimiento</p>
        </div>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nuevo KPI
        </Button>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Resumen Dashboard */}
      {dashboard && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total KPIs</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{dashboard.resumen.total_kpis}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Estado Óptimo</CardTitle>
              <div className="h-3 w-3 rounded-full bg-green-500"></div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{dashboard.resumen.kpis_verdes}</div>
              <p className="text-xs text-muted-foreground">
                {dashboard.resumen.porcentaje_verde.toFixed(1)}% del total
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Requieren Atención</CardTitle>
              <div className="h-3 w-3 rounded-full bg-yellow-500"></div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{dashboard.resumen.kpis_amarillos}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Críticos</CardTitle>
              <div className="h-3 w-3 rounded-full bg-red-500"></div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{dashboard.resumen.kpis_rojos}</div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Lista de KPIs */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {kpis.map((kpi) => (
          <Card key={kpi.id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-2xl">{getTipoIcon(kpi.tipo)}</span>
                  <div>
                    <CardTitle className="text-lg">{kpi.nombre}</CardTitle>
                    <CardDescription>{kpi.descripcion}</CardDescription>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge 
                    className={`${getEstadoColor(kpi.estado)} text-white`}
                  >
                    {getEstadoTexto(kpi.estado)}
                  </Badge>
                  <div className="flex space-x-1">
                    <Button variant="ghost" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="sm">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Progreso */}
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Progreso</span>
                  <span>{kpi.porcentaje_cumplimiento.toFixed(1)}%</span>
                </div>
                <Progress 
                  value={kpi.porcentaje_cumplimiento} 
                  className="h-2"
                />
              </div>

              {/* Valores */}
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <p className="text-gray-600">Valor Actual</p>
                  <p className="font-semibold">
                    {kpi.valor_actual} {kpi.unidad_medida}
                  </p>
                </div>
                <div>
                  <p className="text-gray-600">Objetivo</p>
                  <p className="font-semibold">
                    {kpi.valor_objetivo} {kpi.unidad_medida}
                  </p>
                </div>
              </div>

              {/* Umbrales */}
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>Umbral Amarillo: {kpi.umbral_amarillo}</span>
                <span>Umbral Rojo: {kpi.umbral_rojo}</span>
              </div>

              {/* Tendencia */}
              <div className="flex items-center justify-between pt-2 border-t">
                <span className="text-sm text-gray-600">Tipo: {kpi.tipo}</span>
                <div className="flex items-center space-x-1">
                  {kpi.porcentaje_cumplimiento >= 80 ? (
                    <TrendingUp className="h-4 w-4 text-green-500" />
                  ) : (
                    <TrendingDown className="h-4 w-4 text-red-500" />
                  )}
                  <span className="text-sm">
                    {kpi.porcentaje_cumplimiento >= 80 ? 'En progreso' : 'Requiere atención'}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Estado vacío */}
      {kpis.length === 0 && (
        <Card className="text-center py-12">
          <CardContent>
            <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">No hay KPIs definidos</h3>
            <p className="text-gray-600 mb-4">
              Comience creando indicadores clave para monitorear el rendimiento del proyecto.
            </p>
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Crear Primer KPI
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default KPIsDashboard

