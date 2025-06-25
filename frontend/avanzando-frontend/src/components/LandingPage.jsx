import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  CheckCircle, 
  Users, 
  BarChart3, 
  Shield, 
  Calendar, 
  FileText, 
  AlertTriangle, 
  DollarSign,
  Smartphone,
  Globe,
  ArrowRight,
  Star
} from 'lucide-react'

const LandingPage = ({ onLogin, onRegister }) => {
  const features = [
    {
      icon: <Users className="h-8 w-8 text-blue-600" />,
      title: "Gestión de Proyectos",
      description: "Crea, edita y gestiona proyectos con fases estructuradas y plantillas preconfiguradas."
    },
    {
      icon: <BarChart3 className="h-8 w-8 text-green-600" />,
      title: "KPIs y Dashboards",
      description: "Visualiza el progreso con indicadores de tiempo, alcance y costo en dashboards interactivos."
    },
    {
      icon: <AlertTriangle className="h-8 w-8 text-orange-600" />,
      title: "Gestión de Riesgos",
      description: "Identifica, clasifica y da seguimiento a los riesgos con matriz de probabilidad e impacto."
    },
    {
      icon: <FileText className="h-8 w-8 text-purple-600" />,
      title: "Documentación",
      description: "Genera documentos por fase con plantillas editables y historial de cambios."
    },
    {
      icon: <DollarSign className="h-8 w-8 text-emerald-600" />,
      title: "Control de Costos",
      description: "Registra y liquida actividades con reportes automáticos y comparativas presupuestales."
    },
    {
      icon: <Shield className="h-8 w-8 text-red-600" />,
      title: "Roles y Permisos",
      description: "Control de acceso granular con roles de Administrador, PM, Cliente y Recurso."
    }
  ]

  const plans = [
    {
      name: "Freemium",
      price: "Gratis",
      description: "Perfecto para empezar",
      features: [
        "1 proyecto",
        "Funcionalidades básicas",
        "Sin reportes avanzados",
        "Soporte por email"
      ],
      popular: false
    },
    {
      name: "Estándar",
      price: "$20/mes",
      description: "Para equipos pequeños",
      features: [
        "Hasta 10 proyectos",
        "Reportes y comunicaciones",
        "Dashboard completo",
        "Soporte prioritario"
      ],
      popular: true
    },
    {
      name: "Premium",
      price: "$50/mes",
      description: "Para organizaciones",
      features: [
        "Proyectos ilimitados",
        "IA para predicciones",
        "Integraciones avanzadas",
        "Soporte 24/7"
      ],
      popular: false
    }
  ]

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">Avanzando</h1>
              <Badge variant="secondary" className="ml-3">Beta</Badge>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" onClick={onLogin}>
                Iniciar Sesión
              </Button>
              <Button onClick={onRegister}>
                Crear Cuenta
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Gestión de Proyectos
            <span className="text-blue-600 block">Profesional</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Plataforma integral para la administración de proyectos de tecnología y software, 
            basada en las mejores prácticas de PMI, PM2P, SCRUM y marcos ágiles.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" onClick={onRegister} className="text-lg px-8 py-3">
              Comenzar Gratis
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" onClick={onLogin} className="text-lg px-8 py-3">
              Ver Demo
            </Button>
          </div>
          <div className="mt-12 flex items-center justify-center space-x-6 text-sm text-gray-500">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              Sin tarjeta de crédito
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              Configuración en 2 minutos
            </div>
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              Soporte 24/7
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Todo lo que necesitas para gestionar proyectos
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Herramientas profesionales diseñadas para equipos de desarrollo y consultores
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-center space-x-4">
                    {feature.icon}
                    <CardTitle className="text-xl">{feature.title}</CardTitle>
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Multi-platform Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Accede desde cualquier dispositivo
              </h2>
              <p className="text-xl text-gray-600 mb-8">
                Aplicación web responsive y app móvil nativa para iOS y Android. 
                Mantén el control de tus proyectos desde cualquier lugar.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <div className="flex items-center space-x-3">
                  <Globe className="h-6 w-6 text-blue-600" />
                  <span className="text-lg">Aplicación Web</span>
                </div>
                <div className="flex items-center space-x-3">
                  <Smartphone className="h-6 w-6 text-blue-600" />
                  <span className="text-lg">App Móvil</span>
                </div>
              </div>
            </div>
            <div className="bg-gradient-to-br from-blue-100 to-indigo-200 rounded-lg p-8 text-center">
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <Calendar className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <p className="text-sm font-medium">Cronogramas</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <BarChart3 className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <p className="text-sm font-medium">Reportes</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <Users className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <p className="text-sm font-medium">Equipos</p>
                </div>
                <div className="bg-white rounded-lg p-4 shadow-sm">
                  <Shield className="h-8 w-8 text-red-600 mx-auto mb-2" />
                  <p className="text-sm font-medium">Seguridad</p>
                </div>
              </div>
              <p className="text-gray-600">Sincronización en tiempo real</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Planes que se adaptan a tu equipo
            </h2>
            <p className="text-xl text-gray-600">
              Comienza gratis y escala según tus necesidades
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <Card key={index} className={`relative ${plan.popular ? 'ring-2 ring-blue-500 scale-105' : ''}`}>
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <Badge className="bg-blue-500 text-white px-4 py-1">
                      <Star className="h-4 w-4 mr-1" />
                      Más Popular
                    </Badge>
                  </div>
                )}
                <CardHeader className="text-center">
                  <CardTitle className="text-2xl">{plan.name}</CardTitle>
                  <div className="text-4xl font-bold text-blue-600 my-4">{plan.price}</div>
                  <CardDescription className="text-base">{plan.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-3 mb-6">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center">
                        <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
                        <span>{feature}</span>
                      </li>
                    ))}
                  </ul>
                  <Button 
                    className="w-full" 
                    variant={plan.popular ? "default" : "outline"}
                    onClick={onRegister}
                  >
                    {plan.name === "Freemium" ? "Comenzar Gratis" : "Elegir Plan"}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            ¿Listo para transformar tu gestión de proyectos?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Únete a miles de profesionales que ya confían en Avanzando
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" onClick={onRegister} className="text-lg px-8 py-3">
              Crear Cuenta Gratis
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" onClick={onLogin} className="text-lg px-8 py-3 text-white border-white hover:bg-white hover:text-blue-600">
              Iniciar Sesión
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-blue-400 mb-4">Avanzando</h3>
              <p className="text-gray-400">
                Plataforma profesional para la gestión integral de proyectos de tecnología.
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Producto</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Características</li>
                <li>Precios</li>
                <li>Integraciones</li>
                <li>API</li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Soporte</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Documentación</li>
                <li>Tutoriales</li>
                <li>Centro de Ayuda</li>
                <li>Contacto</li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">Empresa</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Acerca de</li>
                <li>Blog</li>
                <li>Carreras</li>
                <li>Privacidad</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 Avanzando. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

