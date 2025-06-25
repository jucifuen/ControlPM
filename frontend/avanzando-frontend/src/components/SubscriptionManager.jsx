import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Check, Crown, Zap, AlertTriangle, Star } from 'lucide-react'

export default function SubscriptionManager({ user, token }) {
  const [subscription, setSubscription] = useState(null)
  const [plans, setPlans] = useState({})
  const [usage, setUsage] = useState({})
  const [loading, setLoading] = useState(true)
  const [upgrading, setUpgrading] = useState(false)

  useEffect(() => {
    fetchSubscriptionData()
    fetchPlans()
  }, [])

  const fetchSubscriptionData = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/subscription/limits', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        setSubscription(data.subscription)
        setUsage(data.usage)
      }
    } catch (error) {
      console.error('Error fetching subscription:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchPlans = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/plans')
      if (response.ok) {
        const data = await response.json()
        setPlans(data)
      }
    } catch (error) {
      console.error('Error fetching plans:', error)
    }
  }

  const handleUpgrade = async (planType) => {
    setUpgrading(true)
    try {
      const response = await fetch('http://localhost:5000/api/subscription/upgrade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ plan_type: planType })
      })

      if (response.ok) {
        const data = await response.json()
        setSubscription(data.subscription)
        alert(`¡Actualización exitosa a ${planType}!`)
        fetchSubscriptionData()
      } else {
        const error = await response.json()
        alert(`Error: ${error.error}`)
      }
    } catch (error) {
      alert('Error al actualizar suscripción')
    } finally {
      setUpgrading(false)
    }
  }

  const getPlanIcon = (planType) => {
    switch (planType) {
      case 'free': return <Star className="h-5 w-5" />
      case 'pro': return <Crown className="h-5 w-5" />
      case 'enterprise': return <Zap className="h-5 w-5" />
      default: return <Star className="h-5 w-5" />
    }
  }

  const getPlanColor = (planType) => {
    switch (planType) {
      case 'free': return 'bg-gray-100 text-gray-800'
      case 'pro': return 'bg-blue-100 text-blue-800'
      case 'enterprise': return 'bg-purple-100 text-purple-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="flex justify-center p-8">Cargando...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Gestión de Suscripción</h1>
          <p className="text-muted-foreground">Administra tu plan y funcionalidades</p>
        </div>
      </div>

      {/* Plan actual */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            {getPlanIcon(subscription?.plan_type)}
            <span>Plan Actual: {plans[subscription?.plan_type]?.name}</span>
            <Badge className={getPlanColor(subscription?.plan_type)}>
              {subscription?.plan_type?.toUpperCase()}
            </Badge>
          </CardTitle>
          <CardDescription>
            {subscription?.status === 'trial' && subscription?.trial_end_date && (
              <Alert>
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  Período de prueba hasta: {new Date(subscription.trial_end_date).toLocaleDateString()}
                </AlertDescription>
              </Alert>
            )}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <h4 className="font-semibold mb-2">Uso de Proyectos</h4>
              <Progress 
                value={(usage.current_projects / subscription?.limits?.max_projects) * 100} 
                className="mb-2"
              />
              <p className="text-sm text-muted-foreground">
                {usage.current_projects} / {subscription?.limits?.max_projects === -1 ? '∞' : subscription?.limits?.max_projects} proyectos
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Funcionalidades IA</h4>
              <Badge variant={usage.can_use_ai ? 'default' : 'secondary'}>
                {usage.can_use_ai ? 'Disponible' : 'No disponible'}
              </Badge>
            </div>
            <div>
              <h4 className="font-semibold mb-2">Analytics Avanzados</h4>
              <Badge variant={usage.can_use_advanced_analytics ? 'default' : 'secondary'}>
                {usage.can_use_advanced_analytics ? 'Disponible' : 'No disponible'}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Planes disponibles */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {Object.entries(plans).map(([planKey, plan]) => (
          <Card key={planKey} className={`relative ${subscription?.plan_type === planKey ? 'ring-2 ring-blue-500' : ''}`}>
            {subscription?.plan_type === planKey && (
              <Badge className="absolute -top-2 left-4 bg-blue-500">
                Plan Actual
              </Badge>
            )}
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                {getPlanIcon(planKey)}
                <span>{plan.name}</span>
              </CardTitle>
              <CardDescription>
                <span className="text-3xl font-bold">${plan.price}</span>
                <span className="text-muted-foreground">/{plan.billing}</span>
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 mb-6">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-center space-x-2">
                    <Check className="h-4 w-4 text-green-500" />
                    <span className="text-sm">{feature}</span>
                  </li>
                ))}
              </ul>
              
              {subscription?.plan_type !== planKey && planKey !== 'free' && (
                <Button
                  onClick={() => handleUpgrade(planKey)}
                  disabled={upgrading}
                  className="w-full"
                  variant={planKey === 'enterprise' ? 'default' : 'outline'}
                >
                  {upgrading ? 'Actualizando...' : `Actualizar a ${plan.name}`}
                </Button>
              )}
              
              {subscription?.plan_type === planKey && (
                <Button disabled className="w-full" variant="secondary">
                  Plan Actual
                </Button>
              )}
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Límites detallados */}
      <Card>
        <CardHeader>
          <CardTitle>Límites y Funcionalidades</CardTitle>
          <CardDescription>Detalles de tu plan actual</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="text-center p-4 border rounded-lg">
              <h4 className="font-semibold">Proyectos</h4>
              <p className="text-2xl font-bold text-blue-600">
                {subscription?.limits?.max_projects === -1 ? '∞' : subscription?.limits?.max_projects}
              </p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <h4 className="font-semibold">Usuarios por Proyecto</h4>
              <p className="text-2xl font-bold text-green-600">
                {subscription?.limits?.max_users_per_project === -1 ? '∞' : subscription?.limits?.max_users_per_project}
              </p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <h4 className="font-semibold">KPIs por Proyecto</h4>
              <p className="text-2xl font-bold text-purple-600">
                {subscription?.limits?.max_kpis_per_project === -1 ? '∞' : subscription?.limits?.max_kpis_per_project}
              </p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <h4 className="font-semibold">Almacenamiento</h4>
              <p className="text-2xl font-bold text-orange-600">
                {subscription?.limits?.storage_gb} GB
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

