import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { FileText, Upload, Download, Plus, Eye } from 'lucide-react'

export default function DocumentManager({ projectId }) {
  const [documentos, setDocumentos] = useState([])
  const [plantillas, setPlantillas] = useState([])
  const [filtros, setFiltros] = useState({ tipo: 'all', estado: 'all' })
  const [showUpload, setShowUpload] = useState(false)

  useEffect(() => {
    fetchDocumentos()
    fetchPlantillas()
  }, [projectId, filtros])

  const fetchDocumentos = async () => {
    try {
      const params = new URLSearchParams()
      if (projectId) params.append('proyecto_id', projectId)
      if (filtros.tipo !== 'all') params.append('tipo', filtros.tipo)
      
      const response = await fetch(`http://localhost:5000/api/documentos?${params}`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      if (response.ok) {
        const data = await response.json()
        setDocumentos(data.documentos)
      }
    } catch (error) {
      console.error('Error fetching documentos:', error)
    }
  }

  const fetchPlantillas = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/plantillas', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      })
      if (response.ok) {
        const data = await response.json()
        setPlantillas(data.plantillas)
      }
    } catch (error) {
      console.error('Error fetching plantillas:', error)
    }
  }

  const crearDocumento = async (tipo, plantillaId = null) => {
    try {
      const response = await fetch('http://localhost:5000/api/documentos', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          nombre: `Nuevo ${tipo}`,
          tipo,
          proyecto_id: projectId,
          plantilla_id: plantillaId
        })
      })
      if (response.ok) {
        fetchDocumentos()
      }
    } catch (error) {
      console.error('Error creating documento:', error)
    }
  }

  const subirArchivo = async (file) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('http://localhost:5000/api/documentos/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
        body: formData
      })
      if (response.ok) {
        fetchDocumentos()
        setShowUpload(false)
      }
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  }

  const getEstadoBadge = (estado) => {
    const colors = {
      borrador: 'bg-gray-100 text-gray-800',
      revision: 'bg-yellow-100 text-yellow-800',
      aprobado: 'bg-green-100 text-green-800',
      firmado: 'bg-blue-100 text-blue-800'
    }
    return <Badge className={colors[estado]}>{estado}</Badge>
  }

  return (
    <div className="space-y-6">
      {/* Header con filtros */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">Gestión de Documentos</h2>
        <div className="flex gap-2">
          <Select value={filtros.tipo} onValueChange={(value) => setFiltros({...filtros, tipo: value})}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Tipo" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="contrato">Contrato</SelectItem>
              <SelectItem value="propuesta">Propuesta</SelectItem>
              <SelectItem value="informe">Informe</SelectItem>
              <SelectItem value="acta">Acta</SelectItem>
            </SelectContent>
          </Select>
          <Button onClick={() => setShowUpload(true)}>
            <Upload className="w-4 h-4 mr-2" />
            Subir
          </Button>
        </div>
      </div>

      {/* Plantillas rápidas */}
      <Card>
        <CardHeader>
          <CardTitle>Crear desde Plantilla</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {plantillas.map((plantilla) => (
              <Button
                key={plantilla.id}
                variant="outline"
                onClick={() => crearDocumento(plantilla.tipo, plantilla.id)}
                className="h-20 flex flex-col"
              >
                <FileText className="w-6 h-6 mb-2" />
                {plantilla.nombre}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Lista de documentos */}
      <div className="grid gap-4">
        {documentos.map((doc) => (
          <Card key={doc.id}>
            <CardContent className="p-4">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="font-semibold">{doc.nombre}</h3>
                  <p className="text-sm text-gray-600">Tipo: {doc.tipo}</p>
                  <p className="text-sm text-gray-600">Versión: {doc.version}</p>
                </div>
                <div className="flex items-center gap-2">
                  {getEstadoBadge(doc.estado)}
                  <Button size="sm" variant="outline">
                    <Eye className="w-4 h-4" />
                  </Button>
                  <Button size="sm" variant="outline">
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Modal de subida */}
      {showUpload && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <Card className="w-96">
            <CardHeader>
              <CardTitle>Subir Documento</CardTitle>
            </CardHeader>
            <CardContent>
              <Input
                type="file"
                onChange={(e) => e.target.files[0] && subirArchivo(e.target.files[0])}
                accept=".pdf,.doc,.docx,.txt"
              />
              <div className="flex gap-2 mt-4">
                <Button onClick={() => setShowUpload(false)} variant="outline">
                  Cancelar
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

