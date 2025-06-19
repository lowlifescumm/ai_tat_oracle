import { useState } from 'react';
import { Sparkles, Loader2, Star, Moon, Sun, Eye, MapPin, Stars } from 'lucide-react'; // Added Stars, Eye, MapPin

import './App.css';

function App() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    age: '',
    // New personalization fields
    birthplace: '',
    favorite_element: '',
    preferred_aesthetic: '',
    spirit_animal: '',
    life_theme: '',
    personal_story: '',
    cultural_affiliation: ''
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(''); // From first file
  const [loadingStage, setLoadingStage] = useState(''); // From first file
  const [apiError, setApiError] = useState(''); // From first file
  const [showAdvanced, setShowAdvanced] = useState(false); // From second file

  const handleInputChange = (e) => {
    const { name, value } = e.target; // Destructure name and value
    setFormData(prev => ({ // Use functional update for setFormData
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(''); // Clear previous errors
    setResult(null); // Clear previous results
    setLoadingStage('Consulting the mystical oracle...'); // Set initial loading stage

    const API_BASE_URL = 'https://ai-tattoo-api.onrender.com';
    const TIMEOUT_DURATION = 30000; // 30 seconds

    // Create timeout promise
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('The oracle is taking longer than usual. Please try again.')), TIMEOUT_DURATION)
    );

    // Filter out empty optional fields
    const submitData = Object.fromEntries(
      Object.entries(formData).filter(([key, value]) => {
        // Keep required fields even if empty, but they should be validated by 'required' attribute
        if (['first_name', 'last_name', 'date_of_birth', 'age'].includes(key)) {
          return true;
        }
        return value.trim() !== ''; // Filter out empty optional fields
      })
    );

    // Ensure age is an integer
    if (submitData.age) {
      submitData.age = parseInt(submitData.age);
    }

    // Create fetch promise
    const fetchPromise = fetch(`${API_BASE_URL}/api/generate_tattoo`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(submitData)
    });

    try {
      // Race between fetch and timeout
      const response = await Promise.race([fetchPromise, timeoutPromise]);

      if (!response.ok) {
        if (response.status === 500) {
          throw new Error('The mystical forces are temporarily unavailable. Please try again in a moment.');
        } else if (response.status === 429) {
          throw new Error('The oracle is overwhelmed with requests. Please wait a moment before consulting again.');
        } else {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to generate tattoo design');
        }
      }

      setLoadingStage('Channeling cosmic energies...');
      const data = await response.json();

      // Validate response structure
      if (!data.symbolic_analysis || !data.core_tattoo_theme) {
        throw new Error('Received incomplete reading from the oracle. Please try again.');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
      setApiError(err.message); // Set apiError for potential specific messages
    } finally {
      setLoading(false);
      setLoadingStage(''); // Clear loading stage
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white p-4"> {/* Added p-4 for padding */}
      {/* Header */}
      <div className="container mx-auto px-4 py-8 max-w-4xl"> {/* Added max-w-4xl */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center mb-4">
            <Stars className="h-8 w-8 text-yellow-400 mr-2" /> {/* Changed Star to Stars */}
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-yellow-400 to-purple-400 bg-clip-text text-transparent">
              AI Tattoo Oracle Designer {/* Updated title */}
            </h1>
            <Stars className="h-8 w-8 text-yellow-400 ml-2" /> {/* Changed Star to Stars */}
          </div>
          <p className="text-xl text-purple-200 max-w-2xl mx-auto">
            Discover your mystical tattoo destiny through the ancient arts of numerology and astrology {/* Updated description */}
          </p>
        </div>

        {/* Form */}
        <div className="grid md:grid-cols-2 gap-8"> {/* Adjusted to grid layout */}
          <div className="bg-white/10 backdrop-blur-md border-white/20 rounded-2xl p-8"> {/* Card styling */}
            <h2 className="text-white flex items-center gap-2 text-2xl font-bold mb-6"> {/* CardTitle styling */}
              <Sparkles className="text-yellow-400" />
              Enter Your Sacred Details
            </h2>
            <p className="text-purple-200 mb-6"> {/* CardDescription styling */}
              Share your personal information to unlock your unique tattoo design
            </p>
            <form onSubmit={handleSubmit} className="space-y-6"> {/* Adjusted spacing */}
              {/* Required Fields */}
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="first_name"> {/* Added htmlFor */}
                    First Name *
                  </label>
                  <input
                    type="text"
                    id="first_name" // Added id
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                    placeholder="Enter your first name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="last_name"> {/* Added htmlFor */}
                    Last Name *
                  </label>
                  <input
                    type="text"
                    id="last_name" // Added id
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                    placeholder="Enter your last name"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="date_of_birth"> {/* Added htmlFor */}
                    Date of Birth *
                  </label>
                  <input
                    type="text"
                    id="date_of_birth" // Added id
                    name="date_of_birth"
                    value={formData.date_of_birth}
                    onChange={handleInputChange}
                    required
                    placeholder="DD/MM/YYYY"
                    className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="age"> {/* Added htmlFor */}
                    Age *
                  </label>
                  <input
                    type="number"
                    id="age" // Added id
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                    placeholder="Your age"
                  />
                </div>
              </div>

              {/* Advanced Personalization Toggle */}
              <div className="border-t border-purple-500/30 pt-6">
                <button
                  type="button"
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="flex items-center justify-center w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all duration-200"
                >
                  <Moon className="h-5 w-5 mr-2" />
                  {showAdvanced ? 'Hide' : 'Show'} Advanced Personalization
                  <Sparkles className="h-5 w-5 ml-2" />
                </button>
              </div>

              {/* Advanced Fields */}
              {showAdvanced && (
                <div className="space-y-6 border-t border-purple-500/30 pt-6">
                  <div className="text-center mb-4">
                    <p className="text-purple-200 text-sm">
                      Optional fields to deepen your mystical reading
                    </p>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="birthplace">
                        Birthplace
                      </label>
                      <input
                        type="text"
                        id="birthplace"
                        name="birthplace"
                        value={formData.birthplace}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                        placeholder="City or region"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="favorite_element">
                        Favorite Element
                      </label>
                      <select
                        id="favorite_element"
                        name="favorite_element"
                        value={formData.favorite_element}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      >
                        <option value="">Select an element</option>
                        <option value="Fire">🔥 Fire</option>
                        <option value="Water">🌊 Water</option>
                        <option value="Earth">🌍 Earth</option>
                        <option value="Air">💨 Air</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="preferred_aesthetic">
                      Preferred Aesthetic
                    </label>
                    <input
                      type="text"
                      id="preferred_aesthetic"
                      name="preferred_aesthetic"
                      value={formData.preferred_aesthetic}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      placeholder="e.g., Sacred geometry, Celtic, Minimalist, Dark gothic"
                    />
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="spirit_animal">
                        Spirit Animal
                      </label>
                      <input
                        type="text"
                        id="spirit_animal"
                        name="spirit_animal"
                        value={formData.spirit_animal}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                        placeholder="e.g., Phoenix, Wolf, Eagle"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="life_theme">
                        Life Theme/Value
                      </label>
                      <input
                        type="text"
                        id="life_theme"
                        name="life_theme"
                        value={formData.life_theme}
                        onChange={handleInputChange}
                        className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                        placeholder="e.g., Transformation, Freedom, Courage"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="personal_story">
                      Personal Journey (Optional)
                    </label>
                    <textarea
                      id="personal_story"
                      name="personal_story"
                      value={formData.personal_story}
                      onChange={handleInputChange}
                      rows="3"
                      className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      placeholder="Share something meaningful you've overcome or achieved (optional)"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-purple-200 mb-2" htmlFor="cultural_affiliation">
                      Cultural/Spiritual Heritage
                    </label>
                    <input
                      type="text"
                      id="cultural_affiliation"
                      name="cultural_affiliation"
                      value={formData.cultural_affiliation}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 bg-purple-900/50 border border-purple-500/50 rounded-lg text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      placeholder="e.g., Celtic, Norse, Buddhist, Native American"
                    />
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 px-6 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-bold rounded-lg hover:from-purple-700 hover:to-pink-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center" // Combined button styles
              >
                {loading ? (
                  <>
                    <Loader2 className="animate-spin h-5 w-5 mr-2" />
                    <span className="text-purple-200">{loadingStage}</span> {/* Display loading stage */}
                  </>
                ) : (
                  <>
                    <Sparkles className="h-5 w-5 mr-2" /> {/* Sparkles icon for button */}
                    Reveal My Tattoo Destiny
                  </>
                )}
              </button>
              {error && ( // Error message display
                <div className="mt-4 p-3 bg-red-500/20 border border-red-500/30 rounded text-red-200">
                  {error}
                </div>
              )}
            </form>
          </div>

          {/* Results Display */}
          {result && (
            <div className="bg-white/10 backdrop-blur-md border-white/20 rounded-2xl p-8"> {/* Card styling */}
              <h2 className="text-white flex items-center gap-2 text-2xl font-bold mb-6"> {/* CardTitle styling */}
                <Eye className="text-yellow-400" />
                Your Mystical Tattoo Reading
              </h2>
              <div className="space-y-6">
                {/* Dynamic Image Display */}
                {result.image_url ? (
                  <div className="text-center">
                    <img
                      src={`${API_BASE_URL}${result.image_url}`} // Use API_BASE_URL
                      alt="Your Unique Tattoo Design"
                      className="max-w-full h-auto rounded-lg shadow-lg mx-auto border-2 border-yellow-400/30"
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

                {/* Add personalization indicator */}
                {result.personalization_used && Object.values(result.personalization_used).some(Boolean) && ( // Check if any personalization field was used
                  <div className="mt-6 p-4 bg-purple-900/30 rounded-lg border border-purple-500/30">
                    <h3 className="text-lg font-semibold text-yellow-400 mb-2">
                      Personalization Elements Used:
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(result.personalization_used)
                        .filter(([, value]) => value) // Filter to show only used fields
                        .map(([key, value]) => (
                          <span
                            key={key}
                            className="px-3 py-1 bg-purple-600/50 rounded-full text-sm text-purple-200"
                          >
                            {key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </span>
                        ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
