import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Loader2, Stars, Eye, MapPin, Sparkles } from 'lucide-react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    age: ''
  })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [loadingStage, setLoadingStage] = useState('') //
  const [apiError, setApiError] = useState('') //

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setResult(null)
    setLoadingStage('Consulting the mystical oracle...') //

    const API_BASE_URL = 'https://ai-tattoo-api.onrender.com' //
    const TIMEOUT_DURATION = 30000 // 30 seconds

    // Create timeout promise
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('The oracle is taking longer than usual. Please try again.')), TIMEOUT_DURATION)
    )

    // Create fetch promise
    const fetchPromise = fetch(`${API_BASE_URL}/api/generate_tattoo`, { //
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...formData,
        age: parseInt(formData.age)
      })
    })

    try {
      // Race between fetch and timeout
      const response = await Promise.race([fetchPromise, timeoutPromise]) //
      
      if (!response.ok) {
        if (response.status === 500) { //
          throw new Error('The mystical forces are temporarily unavailable. Please try again in a moment.') //
        } else if (response.status === 429) { //
          throw new Error('The oracle is overwhelmed with requests. Please wait a moment before consulting again.') //
        } else {
          const errorData = await response.json() //
          throw new Error(errorData.error || 'Failed to generate tattoo design') //
        }
      }

      setLoadingStage('Channeling cosmic energies...') //
      const data = await response.json()
      
      // Validate response structure
      if (!data.symbolic_analysis || !data.core_tattoo_theme) { //
        throw new Error('Received incomplete reading from the oracle. Please try again.') //
      }
      
      setResult(data)
    } catch (err) {
      setError(err.message) //
      setApiError(err.message) //
    } finally {
      setLoading(false)
      setLoadingStage('') //
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 p-4">
      <div className="container mx-auto max-w-4xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 flex items-center justify-center gap-2">
            <Stars className="text-yellow-400" />
            AI Tattoo Oracle Designer
            <Stars className="text-yellow-400" />
          </h1>
          <p className="text-xl text-purple-200">
            Discover your mystical tattoo destiny through the ancient arts of numerology and astrology
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Input Form */}
          <Card className="bg-white/10 backdrop-blur-md border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <Sparkles className="text-yellow-400" />
                Enter Your Sacred Details
              </CardTitle>
              <CardDescription className="text-purple-200">
                Share your personal information to unlock your unique tattoo design
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <Label htmlFor="first_name" className="text-white">First Name</Label>
                  <Input
                    id="first_name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    required
                    className="bg-white/20 border-white/30 text-white placeholder:text-white/60"
                    placeholder="Enter your first name"
                  />
                </div>
                <div>
                  <Label htmlFor="last_name" className="text-white">Last Name</Label>
                  <Input
                    id="last_name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    required
                    className="bg-white/20 border-white/30 text-white placeholder:text-white/60"
                    placeholder="Enter your last name"
                  />
                </div>
                <div>
                  <Label htmlFor="date_of_birth" className="text-white">Date of Birth</Label>
                  <Input
                    id="date_of_birth"
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleInputChange}
                    required
                    className="bg-white/20 border-white/30 text-white placeholder:text-white/60"
                    placeholder="DD/MM/YYYY"
                  />
                </div>
                <div>
                  <Label htmlFor="age" className="text-white">Age</Label>
                  <Input
                    id="age"
                    name="age"
                    type="number"
                    value={formData.age}
                    onChange={handleInputChange}
                    required
                    className="bg-white/20 border-white/30 text-white placeholder:text-white/60"
                    placeholder="Enter your age"
                  />
                </div>
                <Button 
                  type="submit" 
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                >
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      <span className="text-purple-200">{loadingStage}</span> { /* Updated loading display */ }
                    </>
                  ) : (
                    'Reveal My Tattoo Destiny'
                  )}
                </Button>
              </form>
              {error && (
                <div className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded text-red-200">
                  {error}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results */}
          {result && (
            <Card className="bg-white/10 backdrop-blur-md border-white/20">
              <CardHeader>
                <CardTitle className="text-white flex items-center gap-2">
                  <Eye className="text-yellow-400" />
                  Your Mystical Tattoo Reading
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Dynamic Image Display - NEW SECTION */}
                {result.image_url ? (
                  <div className="text-center">
                    <img 
                      src={`https://ai-tattoo-api.onrender.com${result.image_url}`} 
                      alt="Your Unique Tattoo Design" 
                      className="max-w-full h-auto rounded-lg shadow-lg mx-auto border-2 border-yellow-400/30"
                      // Removed onError, as per your request to just handle the placeholder
                    />
                    <p className="text-sm text-purple-300 mt-2">
                      ✨ Your unique design, crafted by the cosmic forces ✨
                    </p>
                  </div>
                ) : (
                  <div className="text-center p-8 border-2 border-dashed border-yellow-400/30 rounded-lg">
                    <Sparkles className="mx-auto h-12 w-12 text-yellow-400 mb-4" />
                    <p className="text-purple-200">
                      Your mystical reading is complete! Image generation temporarily unavailable.
                    </p>
                  </div>
                )}
                
                <div>
                  <h3 className="text-lg font-semibold text-yellow-400 mb-2">Symbolic Analysis</h3>
                  <p className="text-purple-100">{result.symbolic_analysis}</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-yellow-400 mb-2">Core Theme</h3>
                  <p className="text-purple-100">{result.core_tattoo_theme}</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-yellow-400 mb-2">Visual Motif</h3>
                  <p className="text-purple-100">{result.visual_motif_description}</p>
                </div>
                
                <div>
                  <h3 className="text-lg font-semibold text-yellow-400 mb-2 flex items-center gap-2">
                    <MapPin className="h-4 w-4" />
                    Placement Suggestion
                  </h3>
                  <p className="text-purple-100">{result.placement_suggestion}</p>
                </div>
                
                <div className="border-t border-white/20 pt-4">
                  <h3 className="text-lg font-semibold text-yellow-400 mb-2">Mystical Insight</h3>
                  <p className="text-purple-100 italic font-medium">"{result.mystical_insight}"</p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

export default App;
