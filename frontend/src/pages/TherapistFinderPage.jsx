import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, UserPlus, MapPin, Star, Phone, Mail, Globe, CheckCircle, DollarSign, Video, Users } from 'lucide-react';
import apiService from '../services/api';

const TherapistFinderPage = () => {
  const navigate = useNavigate();
  const [therapists, setTherapists] = useState([]);
  const [states, setStates] = useState([]);
  const [specialties, setSpecialties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [language, setLanguage] = useState(localStorage.getItem('preferredLanguage') || 'en');
  
  // Filters
  const [filters, setFilters] = useState({
    state: '',
    specialty: '',
    language: '',
    max_price: '',
    online_only: false,
  });

  useEffect(() => {
    loadInitialData();
  }, [language]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [statesData, specialtiesData] = await Promise.all([
        apiService.getTherapistStates(language),
        apiService.getTherapistSpecialties(language),
      ]);
      
      setStates(statesData.states || []);
      setSpecialties(specialtiesData.specialties || []);
      
      // Load recommended therapists initially
      await loadRecommendedTherapists();
    } catch (err) {
      console.error('Error loading initial data:', err);
      setError('Failed to load therapist data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const loadRecommendedTherapists = async () => {
    try {
      const sessionId = localStorage.getItem('currentSessionId');
      const response = await apiService.getRecommendedTherapists(sessionId);
      setTherapists(response.therapists || []);
      setError(null);
    } catch (err) {
      console.error('Error loading recommended therapists:', err);
      // Fallback to search with no filters
      handleSearch();
    }
  };

  const handleSearch = async () => {
    try {
      setLoading(true);
      const response = await apiService.searchTherapists(filters);
      setTherapists(response.therapists || []);
      setError(null);
    } catch (err) {
      console.error('Error searching therapists:', err);
      setError('Failed to search therapists. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const handleReset = () => {
    setFilters({
      state: '',
      specialty: '',
      language: '',
      max_price: '',
      online_only: false,
    });
    loadRecommendedTherapists();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-teal-50 to-blue-50">
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
              <div className="bg-gradient-to-r from-green-500 to-teal-500 p-2 rounded-xl">
                <UserPlus className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent">
                  Find a Therapist
                </h1>
                <p className="text-sm text-gray-600">Connect with verified mental health professionals in India</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Search Filters */}
        <div className="mb-8 glass-effect p-6 rounded-xl">
          <h2 className="text-lg font-semibold mb-4 text-gray-800">Search Filters</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {/* State Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">State</label>
              <select
                value={filters.state}
                onChange={(e) => handleFilterChange('state', e.target.value)}
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="">All States</option>
                {states.map((state) => (
                  <option key={state.id} value={state.id}>
                    {state.name} ({state.therapist_count})
                  </option>
                ))}
              </select>
            </div>

            {/* Specialty Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Specialty</label>
              <select
                value={filters.specialty}
                onChange={(e) => handleFilterChange('specialty', e.target.value)}
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="">All Specialties</option>
                {specialties.map((spec) => (
                  <option key={spec.id} value={spec.id}>
                    {spec.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Language Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
              <input
                type="text"
                value={filters.language}
                onChange={(e) => handleFilterChange('language', e.target.value)}
                placeholder="e.g., English, Hindi"
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            {/* Max Price Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Max Price (₹)</label>
              <input
                type="number"
                value={filters.max_price}
                onChange={(e) => handleFilterChange('max_price', e.target.value)}
                placeholder="e.g., 2000"
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />
            </div>

            {/* Online Only Filter */}
            <div className="flex items-center">
              <label className="flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.online_only}
                  onChange={(e) => handleFilterChange('online_only', e.target.checked)}
                  className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                />
                <span className="ml-2 text-sm text-gray-700">Online consultations only</span>
              </label>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-3 mt-6">
            <button
              onClick={handleSearch}
              className="px-6 py-2 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg hover:shadow-lg transition-all"
            >
              Search
            </button>
            <button
              onClick={handleReset}
              className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
            <p className="mt-4 text-gray-600">Finding therapists...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="glass-effect p-6 rounded-xl bg-red-50 border-2 border-red-200">
            <p className="text-red-800">{error}</p>
            <button
              onClick={handleSearch}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Therapists Grid */}
        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {therapists.map((therapist) => (
              <div
                key={therapist.id}
                className="glass-effect rounded-xl overflow-hidden hover:shadow-xl transition-all duration-300"
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-gray-800 mb-1">
                        {therapist.name}
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">{therapist.qualifications}</p>
                      {therapist.verified && (
                        <div className="flex items-center gap-1 text-green-600 text-sm">
                          <CheckCircle className="w-4 h-4" />
                          <span>Verified</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Rating */}
                  <div className="flex items-center gap-2 mb-4">
                    <div className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span className="font-semibold">{therapist.rating}</span>
                    </div>
                    <span className="text-sm text-gray-500">({therapist.reviews_count} reviews)</span>
                  </div>

                  {/* Experience */}
                  <div className="mb-4">
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">{therapist.experience_years} years</span> of experience
                    </p>
                  </div>

                  {/* Specialties */}
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-2">
                      {therapist.specialties?.slice(0, 3).map((spec, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium"
                        >
                          {spec.replace('_', ' ')}
                        </span>
                      ))}
                      {therapist.specialties?.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                          +{therapist.specialties.length - 3} more
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Location */}
                  <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
                    <MapPin className="w-4 h-4" />
                    <span>{therapist.city}, {therapist.state}</span>
                  </div>

                  {/* Languages */}
                  <div className="flex items-center gap-2 text-sm text-gray-600 mb-4">
                    <Users className="w-4 h-4" />
                    <span>{therapist.languages?.join(', ')}</span>
                  </div>

                  {/* Price */}
                  <div className="flex items-center gap-2 text-sm font-semibold text-gray-800 mb-4">
                    <DollarSign className="w-4 h-4" />
                    <span>₹{therapist.consultation_fee_min} - ₹{therapist.consultation_fee_max}</span>
                  </div>

                  {/* Availability */}
                  <div className="flex gap-2 mb-4">
                    {therapist.online_available && (
                      <span className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                        <Video className="w-3 h-3" />
                        Online
                      </span>
                    )}
                    {therapist.in_person_available && (
                      <span className="px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs">
                        In-person
                      </span>
                    )}
                  </div>

                  {/* About */}
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {therapist.about}
                  </p>

                  {/* Contact Buttons */}
                  <div className="grid grid-cols-2 gap-2">
                    {therapist.contact_phone && (
                      <a
                        href={`tel:${therapist.contact_phone}`}
                        className="flex items-center justify-center gap-2 px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-all text-sm"
                      >
                        <Phone className="w-4 h-4" />
                        Call
                      </a>
                    )}
                    {therapist.website && (
                      <a
                        href={therapist.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-center gap-2 px-3 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-all text-sm"
                      >
                        <Globe className="w-4 h-4" />
                        Website
                      </a>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && therapists.length === 0 && (
          <div className="text-center py-12 glass-effect rounded-xl">
            <UserPlus className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No therapists found</h3>
            <p className="text-gray-600 mb-4">Try adjusting your search filters</p>
            <button
              onClick={handleReset}
              className="px-6 py-2 bg-gradient-to-r from-green-500 to-teal-500 text-white rounded-lg hover:shadow-lg transition-all"
            >
              Show All Therapists
            </button>
          </div>
        )}

        {/* Disclaimer */}
        <div className="mt-8 glass-effect p-6 rounded-xl bg-yellow-50 border-2 border-yellow-200">
          <p className="text-sm text-yellow-800">
            <strong>Disclaimer:</strong> Please verify therapist credentials and availability before booking. 
            This directory is for informational purposes only. Always ensure the therapist is registered with 
            appropriate professional bodies (RCI, MCI, etc.).
          </p>
        </div>
      </main>
    </div>
  );
};

export default TherapistFinderPage;

