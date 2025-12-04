import { useState, useEffect } from 'react';
import { X, Plus, Trash2, Phone, MessageSquare, MapPin, AlertCircle, CheckCircle } from 'lucide-react';

const EmergencySetup = ({ sessionId, onComplete, onSkip }) => {
  const [contacts, setContacts] = useState([{
    name: '',
    phone: '',
    relationship: 'Family',
    whatsapp_enabled: true
  }]);
  const [locationPermission, setLocationPermission] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [hasExisting, setHasExisting] = useState(false);

  const relationships = ['Family', 'Friend', 'Partner', 'Therapist', 'Other'];

  useEffect(() => {
    checkExistingSetup();
  }, [sessionId]);

  const checkExistingSetup = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/emergency/contacts/check/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        if (data.setup_completed) {
          setHasExisting(true);
          // Load existing contacts
          loadExistingContacts();
        }
      }
    } catch (err) {
      console.error('Error checking setup:', err);
    }
  };

  const loadExistingContacts = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/emergency/contacts/${sessionId}`);
      if (response.ok) {
        const data = await response.json();
        setContacts(data.contacts);
        setLocationPermission(data.location_permission);
      }
    } catch (err) {
      console.error('Error loading contacts:', err);
    }
  };

  const addContact = () => {
    if (contacts.length < 3) {
      setContacts([...contacts, {
        name: '',
        phone: '',
        relationship: 'Family',
        whatsapp_enabled: true
      }]);
    }
  };

  const removeContact = (index) => {
    if (contacts.length > 1) {
      setContacts(contacts.filter((_, i) => i !== index));
    }
  };

  const updateContact = (index, field, value) => {
    const newContacts = [...contacts];
    newContacts[index][field] = value;
    setContacts(newContacts);
  };

  const validatePhone = (phone) => {
    // Check if phone starts with + and has 10-15 digits
    const cleaned = phone.replace(/[\s\-]/g, '');
    return /^\+\d{10,15}$/.test(cleaned);
  };

  const validateForm = () => {
    // Check all contacts have name and valid phone
    for (let contact of contacts) {
      if (!contact.name.trim()) {
        setError('Please enter a name for all contacts');
        return false;
      }
      if (!contact.phone.trim()) {
        setError('Please enter a phone number for all contacts');
        return false;
      }
      if (!validatePhone(contact.phone)) {
        setError('Phone numbers must start with + and country code (e.g., +919876543210)');
        return false;
      }
    }
    return true;
  };

  const handleSave = async () => {
    setError('');
    setSuccess('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `http://localhost:8000/api/emergency/contacts/save?session_id=${sessionId}&location_permission=${locationPermission}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(contacts),
        }
      );

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to save contacts');
      }

      setSuccess('Emergency contacts saved successfully! ✅');
      setTimeout(() => {
        onComplete();
      }, 1500);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const requestLocationPermission = () => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        () => {
          setLocationPermission(true);
          setSuccess('Location permission granted ✅');
          setTimeout(() => setSuccess(''), 3000);
        },
        (err) => {
          setError('Location permission denied. You can still save contacts.');
          setTimeout(() => setError(''), 3000);
        }
      );
    } else {
      setError('Geolocation is not supported by your browser');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-red-500 to-pink-600 p-6 rounded-t-2xl">
          <div className="flex justify-between items-start">
            <div>
              <h2 className="text-2xl font-bold text-white mb-2">
                🆘 Emergency Contact Setup
              </h2>
              <p className="text-white text-opacity-90 text-sm">
                {hasExisting ? 'Update your emergency contacts' : 'Set up trusted contacts who will be notified in case of crisis'}
              </p>
            </div>
            {onSkip && !hasExisting && (
              <button
                onClick={onSkip}
                className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors"
              >
                <X size={24} />
              </button>
            )}
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex gap-3">
            <AlertCircle className="text-blue-600 flex-shrink-0" size={20} />
            <div className="text-sm text-blue-800">
              <p className="font-semibold mb-1">Why do we need this?</p>
              <p>In case of a mental health crisis, we can instantly alert your trusted contacts with your location and relevant information to help you get support quickly.</p>
            </div>
          </div>

          {/* Contacts */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-800">
                Emergency Contacts (1-3)
              </h3>
              {contacts.length < 3 && (
                <button
                  onClick={addContact}
                  className="flex items-center gap-2 px-3 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm font-medium"
                >
                  <Plus size={16} />
                  Add Contact
                </button>
              )}
            </div>

            {contacts.map((contact, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium text-gray-600">
                    Contact {index + 1}
                  </span>
                  {contacts.length > 1 && (
                    <button
                      onClick={() => removeContact(index)}
                      className="text-red-500 hover:bg-red-50 p-1 rounded transition-colors"
                    >
                      <Trash2 size={16} />
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Name *
                    </label>
                    <input
                      type="text"
                      value={contact.name}
                      onChange={(e) => updateContact(index, 'name', e.target.value)}
                      placeholder="John Doe"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Relationship *
                    </label>
                    <select
                      value={contact.relationship}
                      onChange={(e) => updateContact(index, 'relationship', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      {relationships.map(rel => (
                        <option key={rel} value={rel}>{rel}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone Number * (with country code)
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
                    <input
                      type="tel"
                      value={contact.phone}
                      onChange={(e) => updateContact(index, 'phone', e.target.value)}
                      placeholder="+919876543210"
                      className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    />
                  </div>
                  <p className="text-xs text-gray-500 mt-1">
                    Format: +[country code][number] (e.g., +919876543210 for India)
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id={`whatsapp-${index}`}
                    checked={contact.whatsapp_enabled}
                    onChange={(e) => updateContact(index, 'whatsapp_enabled', e.target.checked)}
                    className="w-4 h-4 text-purple-600 border-gray-300 rounded focus:ring-purple-500"
                  />
                  <label htmlFor={`whatsapp-${index}`} className="text-sm text-gray-700 flex items-center gap-1">
                    <MessageSquare size={14} className="text-green-600" />
                    Send WhatsApp messages
                  </label>
                </div>
              </div>
            ))}
          </div>

          {/* Location Permission */}
          <div className="border border-gray-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <MapPin className="text-purple-600 flex-shrink-0 mt-1" size={20} />
              <div className="flex-1">
                <h4 className="font-semibold text-gray-800 mb-1">Location Sharing</h4>
                <p className="text-sm text-gray-600 mb-3">
                  Allow us to share your location with emergency contacts during a crisis
                </p>
                <button
                  onClick={requestLocationPermission}
                  disabled={locationPermission}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    locationPermission
                      ? 'bg-green-100 text-green-700 cursor-not-allowed'
                      : 'bg-purple-600 text-white hover:bg-purple-700'
                  }`}
                >
                  {locationPermission ? (
                    <span className="flex items-center gap-2">
                      <CheckCircle size={16} />
                      Permission Granted
                    </span>
                  ) : (
                    'Grant Permission'
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Error/Success Messages */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-700 text-sm">
              {error}
            </div>
          )}
          {success && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-3 text-green-700 text-sm">
              {success}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <button
              onClick={handleSave}
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-lg font-semibold hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Saving...' : hasExisting ? 'Update Contacts' : 'Save & Continue'}
            </button>
            {onSkip && !hasExisting && (
              <button
                onClick={onSkip}
                className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
              >
                Skip for Now
              </button>
            )}
          </div>

          <p className="text-xs text-gray-500 text-center">
            Your emergency contacts will only be notified if you trigger an emergency alert or if our system detects a crisis situation.
          </p>
        </div>
      </div>
    </div>
  );
};

export default EmergencySetup;

