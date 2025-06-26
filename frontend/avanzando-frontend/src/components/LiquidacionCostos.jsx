import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Plus, Trash2, Calculator, FileText } from 'lucide-react'

export default function LiquidacionCostos({ projectId }) {
  const [liquidaciones, setLiquidaciones] = useState([])
  const [liquidacionActual, setLiquidacionActual] = useState(null)
  const [gastos, setGastos] = useState([])
  const [horas, setHoras] = useState([])
  const [nuevoGasto, setNuevoGasto] = useState({
    tipo_gasto: 'material',
    descripcion: '',
    cantidad: 1,
    precio_unitario: 0
  })

  useEffect(() => {
    fetchLiquidaciones()
  }, [projectId])

  const fetchLiquidaciones = async () => {
    try {
      const response = await fetch(`http://localhost:5000/api/liquidaciones?proyecto_id=${projectId}`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      if (response.ok) {
        const data = await response.json()
        setLiquidaciones(data.liquidaciones)
      }
    } catch (error) {
      console.error('Error fetching liquidaciones:', error)
    }
  }

  const crearLiquidacion = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/liquidaciones', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          proyecto_id: projectId,
          periodo_inicio: new Date().toISOString().split('T')[0],
          periodo_fin: new Date().toISOString().split('T')[0]
        })
      })
      if (response.ok) {
        const data = await response.json()
        setLiquidacionActual(data.liquidacion)
        fetchLiquidaciones()
      }
    } catch (error) {
      console.error('Error creating liquidacion:', error)
    }
  }

  const agregarGasto = async () => {
    if (!liquidacionActual) return
    
    try {
      const total = nuevoGasto.cantidad * nuevoGasto.precio_unitario
      const response = await fetch('http://localhost:5000/api/liquidaciones/gastos', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          liquidacion_id: liquidacionActual.id,
          ...nuevoGasto,
          total,
          fecha_gasto: new Date().toISOString().split('T')[0]
        })
      })
      if (response.ok) {
        setNuevoGasto({
          tipo_gasto: 'material',
          descripcion: '',
          cantidad: 1,
          precio_unitario: 0
        })
        fetchGastos()
      }
    } catch (error) {
      console.error('Error adding gasto:', error)
    }
  }

  const fetchGastos = async () => {
    if (!liquidacionActual) return
    
    try {
      const response = await fetch(`http://localhost:5000/api/liquidaciones/${liquidacionActual.id}/gastos`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      if (response.ok) {
        const data = await response.json()
        setGastos(data.gastos)
      }
    } catch (error) {
      console.error('Error fetching gastos:', error)
    }
  }

  const calcularTotal = () => {
    return gastos.reduce((sum, gasto) => sum + gasto.total, 0)
  }

  const generarReporte = async () => {
    if (!liquidacionActual) return
    
    try {
      const response = await fetch(`http://localhost:5000/api/liquidaciones/${liquidacionActual.id}/reporte`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `liquidacion-${liquidacionActual.id}.pdf`
        a.click()
      }
    } catch (error) {
      console.error('Error generating report:', error)
    }
  }

  const getEstadoBadge = (estado) => {
    const colors = {
      borrador: 'bg-gray-100 text-gray-800',
      enviada: 'bg-blue-100 text-blue-800',
      aprobada: 'bg-green-100 text-green-800',
      pagada: 'bg-purple-100 text-purple-800',
      rechazada: 'bg-red-100 text-red-800'
    }
    return <Badge className={colors[estado]}>{estado}</Badge>
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Liquidación de Costos</h2>
        <Button onClick={crearLiquidacion}>
          <Plus className="w-4 h-4 mr-2" />
          Nueva Liquidación
        </Button>
      </div>

      {/* Lista de liquidaciones */}
      <Card>
        <CardHeader>
          <CardTitle>Liquidaciones del Proyecto</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {liquidaciones.map((liquidacion) => (
              <div key={liquidacion.id} className="flex justify-between items-center p-4 border rounded">
                <div>
                  <p className="font-semibold">Período: {liquidacion.periodo_inicio} - {liquidacion.periodo_fin}</p>
                  <p className="text-sm text-gray-600">Total: ${liquidacion.total_gastos}</p>
                </div>
                <div className="flex items-center gap-2">
                  {getEstadoBadge(liquidacion.estado)}
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setLiquidacionActual(liquidacion)}
                  >
                    Editar
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Editor de liquidación actual */}
      {liquidacionActual && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Agregar gastos */}
          <Card>
            <CardHeader>
              <CardTitle>Agregar Gasto</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Select 
                value={nuevoGasto.tipo_gasto} 
                onValueChange={(value) => setNuevoGasto({...nuevoGasto, tipo_gasto: value})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="personal">Personal</SelectItem>
                  <SelectItem value="material">Material</SelectItem>
                  <SelectItem value="servicio">Servicio</SelectItem>
                  <SelectItem value="transporte">Transporte</SelectItem>
                  <SelectItem value="otro">Otro</SelectItem>
                </SelectContent>
              </Select>
              
              <Input
                placeholder="Descripción del gasto"
                value={nuevoGasto.descripcion}
                onChange={(e) => setNuevoGasto({...nuevoGasto, descripcion: e.target.value})}
              />
              
              <div className="grid grid-cols-2 gap-2">
                <Input
                  type="number"
                  placeholder="Cantidad"
                  value={nuevoGasto.cantidad}
                  onChange={(e) => setNuevoGasto({...nuevoGasto, cantidad: parseFloat(e.target.value)})}
                />
                <Input
                  type="number"
                  placeholder="Precio unitario"
                  value={nuevoGasto.precio_unitario}
                  onChange={(e) => setNuevoGasto({...nuevoGasto, precio_unitario: parseFloat(e.target.value)})}
                />
              </div>
              
              <div className="flex justify-between items-center">
                <span className="font-semibold">
                  Total: ${(nuevoGasto.cantidad * nuevoGasto.precio_unitario).toFixed(2)}
                </span>
                <Button onClick={agregarGasto}>
                  <Plus className="w-4 h-4 mr-2" />
                  Agregar
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Resumen */}
          <Card>
            <CardHeader>
              <CardTitle>Resumen de Gastos</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center text-lg font-semibold">
                  <span>Total General:</span>
                  <span>${calcularTotal().toFixed(2)}</span>
                </div>
                
                <div className="flex gap-2">
                  <Button onClick={generarReporte} className="flex-1">
                    <FileText className="w-4 h-4 mr-2" />
                    Generar Reporte
                  </Button>
                  <Button variant="outline" className="flex-1">
                    <Calculator className="w-4 h-4 mr-2" />
                    Calcular
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Lista de gastos */}
      {liquidacionActual && gastos.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Detalle de Gastos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Tipo</th>
                    <th className="text-left p-2">Descripción</th>
                    <th className="text-right p-2">Cantidad</th>
                    <th className="text-right p-2">Precio Unit.</th>
                    <th className="text-right p-2">Total</th>
                    <th className="text-center p-2">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {gastos.map((gasto) => (
                    <tr key={gasto.id} className="border-b">
                      <td className="p-2">{gasto.tipo_gasto}</td>
                      <td className="p-2">{gasto.descripcion}</td>
                      <td className="text-right p-2">{gasto.cantidad}</td>
                      <td className="text-right p-2">${gasto.precio_unitario}</td>
                      <td className="text-right p-2">${gasto.total}</td>
                      <td className="text-center p-2">
                        <Button size="sm" variant="outline">
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

