import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { Brain, TrendingUp, AlertTriangle, Calendar, Target, DollarSign, Sparkles, Crown } from 'lucide-react'

export default function AIInsights({ project, token }) {
  const [insights, setInsights] = useState(null)
  const [predictions, setPredictions] = useState([])
  const [loading, setLoading] = useState(false)
  const [hasAIAccess, setHasAIAccess] = useState(false)

  useEffect(() => {
    checkAIAccess()
    if (project) {
      fetchInsights()
      fetchPredictions()
    }
  }, [project])

  const checkAIAccess = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/subscription/check-limit/ai_features', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setHasAIAccess(data.allowed)
      }
    } catch (error) {
      console.error('Error checking AI access:', error)
    }
  }

  const fetchInsights = async () => {
    if (!hasAIAccess) return
    
    setLoading(true)
    try {
      const response = await fetch(`http://localhost:5000/api/ai/insights/${project.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setInsights(data)
      }
    } catch (error) {
      console.error('Error fetching insights:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPredictions = async () => {
    if (!hasAIAccess) return
    
    try {
      const response = await fetch(`http://localhost:5000/api/ai/predictions/${project.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setPredictions(data.predictions)
      }
    } catch (error) {
      console.error('Error fetching predictions:', error)
    }
  }

  const runPrediction = async (type) => {
    setLoading(true)
    try {
      let endpoint = ''
      switch (type) {
        case 'completion':
          endpoint = `http://localhost:5000/api/ai/predict/project-completion/${project.id}`
          break
        case 'budget':
          endpoint = `http://localhost:5000/api/ai/predict/budget-overrun/${project.id}`
          break
        default:
          return
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })

      if (response.ok) {
        fetchPredictions()
        fetchInsights()
      } else {
        const error = await response.json()
        alert(`Error: ${error.error}`)
      }
    } catch (error) {
      alert('Error al ejecutar predicción')
    } finally {
      setLoading(false)
    }
  }

  const getHealthColor = (health) => {
    switch (health) {
      case 'good': return 'text-green-600'
      case 'warning': return 'text-yellow-600'
      case 'critical': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getHealthBadge = (health) => {
    switch (health) {
      case 'good': return <Badge className="bg-green-100 text-green-800">Saludable</Badge>
      case 'warning': return <Badge className="bg-yellow-100 text-yellow-800">Atención</Badge>
      case 'critical': return <Badge className="bg-red-100 text-red-800">Crítico</Badge>
      default: return <Badge variant="secondary">Desconocido</Badge>
    }
  }

  if (!hasAIAccess) {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Crown className="h-5 w-5 text-yellow-500" />
              <span>Funcionalidades de IA Premium</span>
            </CardTitle>
            <CardDescription>
              Desbloquea insights avanzados y predicciones con IA
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center py-8">
            <Brain className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold mb-2">Actualiza para acceder a IA</h3>
            <p className="text-muted-foreground mb-6">
              Las funcionalidades de inteligencia artificial están disponibles en los planes Pro y Enterprise.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div className="text-left p-4 border rounded-lg">
                <h4 className="font-semibold mb-2">Predicciones de Proyecto</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Fecha de finalización estimada</li>
                  <li>• Probabilidad de sobrecosto</li>
                  <li>• Análisis de riesgos</li>
                </ul>
              </div>
              <div className="text-left p-4 border rounded-lg">
                <h4 className="font-semibold mb-2">Insights Avanzados</h4>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• Salud general del proyecto</li>
                  <li>• Recomendaciones automáticas</li>
                  <li>• Tendencias de KPIs</li>
                </ul>
              </div>
            </div>
            <Button className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600">
              <Crown className="h-4 w-4 mr-2" />
              Actualizar Plan
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center space-x-2">
            <Sparkles className="h-6 w-6 text-purple-500" />
            <span>Insights de IA</span>
          </h2>
          <p className="text-muted-foreground">Análisis inteligente del proyecto</p>
        </div>
        <div className="flex space-x-2">
          <Button
            onClick={() => runPrediction('completion')}
            disabled={loading}
            variant="outline"
          >
            <Calendar className="h-4 w-4 mr-2" />
            Predecir Finalización
          </Button>
          <Button
            onClick={() => runPrediction('budget')}
            disabled={loading}
            variant="outline"
          >
            <DollarSign className="h-4 w-4 mr-2" />
            Análisis Presupuesto
          </Button>
        </div>
      </div>

      {/* Salud del proyecto */}
      {insights && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Brain className="h-5 w-5" />
              <span>Salud del Proyecto</span>
              {getHealthBadge(insights.project_health)}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center">
                <h4 className="font-semibold mb-2">Probabilidad de Éxito</h4>
                <div className="relative">
                  <Progress value={insights.completion_likelihood * 100} className="mb-2" />
                  <span className="text-2xl font-bold text-green-600">
                    {Math.round(insights.completion_likelihood * 100)}%
                  </span>
                </div>
              </div>
              <div className="text-center">
                <h4 className="font-semibold mb-2">Estado Presupuesto</h4>
                <Badge variant={insights.budget_status === 'on_track' ? 'default' : 'destructive'}>
                  {insights.budget_status === 'on_track' ? 'En Curso' : 'En Riesgo'}
                </Badge>
              </div>
              <div className="text-center">
                <h4 className="font-semibold mb-2">Riesgos Críticos</h4>
                <span className="text-2xl font-bold text-red-600">
                  {insights.key_risks}
                </span>
              </div>
              <div className="text-center">
                <h4 className="font-semibold mb-2">Rendimiento KPIs</h4>
                <Badge variant="secondary">
                  {insights.kpi_performance}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Recomendaciones */}
      {insights?.recommendations && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>Recomendaciones de IA</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {insights.recommendations.map((recommendation, index) => (
                <Alert key={index}>
                  <TrendingUp className="h-4 w-4" />
                  <AlertDescription>{recommendation}</AlertDescription>
                </Alert>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Predicciones recientes */}
      {predictions.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Predicciones Recientes</CardTitle>
            <CardDescription>Análisis generados por IA</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {predictions.slice(0, 5).map((prediction) => (
                <div key={prediction.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold">
                      {prediction.prediction_type.replace('_', ' ').toUpperCase()}
                    </h4>
                    <Badge variant="outline">
                      Confianza: {Math.round(prediction.confidence_score * 100)}%
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">
                    {new Date(prediction.created_at).toLocaleString()}
                  </p>
                  
                  {prediction.prediction_type === 'project_completion' && prediction.prediction_result && (
                    <div className="space-y-2">
                      <p>
                        <strong>Días estimados para completar:</strong> {prediction.prediction_result.estimated_completion_days}
                      </p>
                      <p>
                        <strong>Probabilidad de éxito:</strong> {Math.round(prediction.prediction_result.completion_probability * 100)}%
                      </p>
                    </div>
                  )}
                  
                  {prediction.prediction_type === 'budget_overrun' && prediction.prediction_result && (
                    <div className="space-y-2">
                      <p>
                        <strong>Probabilidad de sobrecosto:</strong> {Math.round(prediction.prediction_result.overrun_probability * 100)}%
                      </p>
                      <p>
                        <strong>Costo proyectado:</strong> {Math.round(prediction.prediction_result.projected_cost_percentage)}%
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {loading && (
        <Card>
          <CardContent className="text-center py-8">
            <Brain className="h-8 w-8 animate-pulse text-purple-500 mx-auto mb-4" />
            <p>Generando insights con IA...</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

