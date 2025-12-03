import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Heart, Clock, TrendingUp, ExternalLink, Play } from 'lucide-react';
import apiService from '../services/api';

const CopingStrategiesPage = () => {
  const navigate = useNavigate();
  const [strategies, setStrategies] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedStrategy, setExpandedStrategy] = useState(null);
  const [language, setLanguage] = useState(localStorage.getItem('preferredLanguage') || 'en');

  useEffect(() => {
    loadStrategies();
    loadCategories();
  }, [selectedCategory, language]);

  const loadStrategies = async () => {
    try {
      setLoading(true);
      const sessionId = localStorage.getItem('currentSessionId');
      
      let response;
      if (selectedCategory === 'all' && sessionId) {
        // Get personalized strategies
        response = await apiService.getPersonalizedStrategies(sessionId, language);
      } else if (selectedCategory === 'all') {
        response = await apiService.getAllStrategies(null, language);
      } else {
        response = await apiService.getAllStrategies(selectedCategory, language);
      }
      
      setStrategies(response.strategies || []);
      setError(null);
    } catch (err) {
      console.error('Error loading strategies:', err);
      setError('Failed to load coping strategies. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await apiService.getCopingCategories(language);
      setCategories(response.categories || []);
    } catch (err) {
      console.error('Error loading categories:', err);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      breathing: 'bg-blue-100 text-blue-800',
      grounding: 'bg-purple-100 text-purple-800',
      mindfulness: 'bg-green-100 text-green-800',
      cbt: 'bg-orange-100 text-orange-800',
      physical: 'bg-pink-100 text-pink-800',
    };
    return colors[category] || 'bg-gray-100 text-gray-800';
  };

  const getYouTubeEmbedUrl = (url) => {
    if (!url) return null;
    const videoId = url.split('v=')[1]?.split('&')[0] || url.split('/').pop();
    return `https://www.youtube.com/embed/${videoId}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="glass-effect border-b border-white/20 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/')}
              className="glass-effect p-2 rounded-lg hover:shadow-lg transition-all"
              aria-label="Back to chat"
            >
              <ArrowLeft className="w-5 h-5 text-gray-700" />
            </button>
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-r from-primary-500 to-secondary-500 p-2 rounded-xl">
                <Heart className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-secondary-600 bg-clip-text text-transparent">
                  Coping Strategies
                </h1>
                <p className="text-sm text-gray-600">Evidence-based techniques for your wellbeing</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Category Filter */}
        <div className="mb-8 glass-effect p-6 rounded-xl">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Filter by Category</h2>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setSelectedCategory('all')}
              className={`px-4 py-2 rounded-lg transition-all ${
                selectedCategory === 'all'
                  ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg'
                  : 'bg-white text-gray-700 hover:shadow-md'
              }`}
            >
              All Strategies
            </button>
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-4 py-2 rounded-lg transition-all ${
                  selectedCategory === cat.id
                    ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg'
                    : 'bg-white text-gray-700 hover:shadow-md'
                }`}
              >
                {cat.name}
              </button>
            ))}
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading strategies...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="glass-effect p-6 rounded-xl bg-red-50 border-2 border-red-200">
            <p className="text-red-800">{error}</p>
            <button
              onClick={loadStrategies}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Strategies Grid */}
        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {strategies.map((strategy) => (
              <div
                key={strategy.id}
                className="glass-effect rounded-xl overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-800 mb-2">
                        {strategy.name}
                      </h3>
                      <div className="flex flex-wrap gap-2 mb-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getCategoryColor(strategy.category)}`}>
                          {strategy.category}
                        </span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(strategy.difficulty)}`}>
                          {strategy.difficulty}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-600 mb-4 line-clamp-3">
                    {strategy.description}
                  </p>

                  {/* Meta Info */}
                  <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                    <div className="flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      <span>{strategy.duration_minutes} min</span>
                    </div>
                    <div className="flex items-center gap-1">
                      <TrendingUp className="w-4 h-4" />
                      <span>Effective</span>
                    </div>
                  </div>

                  {/* Expand Button */}
                  <button
                    onClick={() => setExpandedStrategy(expandedStrategy === strategy.id ? null : strategy.id)}
                    className="w-full px-4 py-2 bg-gradient-to-r from-primary-500 to-secondary-500 text-white rounded-lg hover:shadow-lg transition-all"
                  >
                    {expandedStrategy === strategy.id ? 'Show Less' : 'Learn More'}
                  </button>

                  {/* Expanded Content */}
                  {expandedStrategy === strategy.id && (
                    <div className="mt-6 pt-6 border-t border-gray-200">
                      {/* Steps */}
                      <div className="mb-6">
                        <h4 className="font-semibold text-gray-800 mb-3">How to do it:</h4>
                        <ol className="space-y-2">
                          {strategy.steps?.map((step, index) => (
                            <li key={index} className="text-sm text-gray-700 flex gap-2">
                              <span className="font-semibold text-primary-600">{index + 1}.</span>
                              <span>{step}</span>
                            </li>
                          ))}
                        </ol>
                      </div>

                      {/* Video */}
                      {strategy.video_url && (
                        <div className="mb-6">
                          <h4 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                            <Play className="w-4 h-4" />
                            Video Guide:
                          </h4>
                          <div className="aspect-video rounded-lg overflow-hidden">
                            <iframe
                              src={getYouTubeEmbedUrl(strategy.video_url)}
                              title={strategy.name}
                              className="w-full h-full"
                              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                              allowFullScreen
                            ></iframe>
                          </div>
                        </div>
                      )}

                      {/* Scientific Basis */}
                      {strategy.scientific_basis && (
                        <div className="mb-6">
                          <h4 className="font-semibold text-gray-800 mb-2">Scientific Basis:</h4>
                          <p className="text-sm text-gray-600 italic">{strategy.scientific_basis}</p>
                        </div>
                      )}

                      {/* External Links */}
                      {strategy.external_links && strategy.external_links.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-800 mb-2">Learn More:</h4>
                          <div className="space-y-2">
                            {strategy.external_links.map((link, index) => (
                              <a
                                key={index}
                                href={link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 text-sm text-primary-600 hover:text-primary-700"
                              >
                                <ExternalLink className="w-4 h-4" />
                                <span>Resource {index + 1}</span>
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && strategies.length === 0 && (
          <div className="text-center py-12 glass-effect rounded-xl">
            <Heart className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No strategies found</h3>
            <p className="text-gray-600">Try selecting a different category</p>
          </div>
        )}
      </main>
    </div>
  );
};

export default CopingStrategiesPage;

