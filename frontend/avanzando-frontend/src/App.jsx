import { useState, useEffect } from 'react'
import LandingPage from './components/LandingPage'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [currentView, setCurrentView] = useState('landing') // 'landing', 'login', 'register', 'dashboard'
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Verificar si hay una sesión guardada
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
      setCurrentView('dashboard')
    }
    
    setLoading(false)
  }, [])

  const handleLogin = (userData, userToken) => {
    setUser(userData)
    setToken(userToken)
    setCurrentView('dashboard')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    setToken(null)
    setCurrentView('landing')
  }

  const handleRegisterSuccess = () => {
    setCurrentView('login')
  }

  const navigateToLogin = () => {
    setCurrentView('login')
  }

  const navigateToRegister = () => {
    setCurrentView('register')
  }

  const navigateToLanding = () => {
    setCurrentView('landing')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  // Si el usuario está autenticado, mostrar dashboard
  if (user && token && currentView === 'dashboard') {
    return (
      <Dashboard 
        user={user} 
        token={token} 
        onLogout={handleLogout} 
      />
    )
  }

  // Navegación basada en la vista actual
  switch (currentView) {
    case 'login':
      return (
        <Login 
          onLogin={handleLogin}
          onBackToLanding={navigateToLanding}
          onGoToRegister={navigateToRegister}
        />
      )
    case 'register':
      return (
        <Register 
          onRegister={handleRegisterSuccess}
          onBackToLanding={navigateToLanding}
        />
      )
    case 'landing':
    default:
      return (
        <LandingPage 
          onLogin={navigateToLogin}
          onRegister={navigateToRegister}
        />
      )
  }
}

export default App
