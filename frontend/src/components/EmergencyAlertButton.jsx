import { useState } from 'react';
import { AlertCircle, MapPin, Send, Loader, CheckCircle, XCircle } from 'lucide-react';

const EmergencyAlertButton = ({ sessionId, crisisContext, userName }) => {
  const [showConfirm, setShowConfirm] = useState(false);
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState(null);
  const [location, setLocation] = useState(null);

  const getLocation = () => {
    return new Promise((resolve, reject) => {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            resolve({
              latitude: position.coords.latitude,
              longitude: position.coords.longitude,
              accuracy: position.coords.accuracy
            });
          },
          (error) => {
            // If location fails, resolve with null
            console.error('Location error:', error);
            resolve({
              latitude: null,
              longitude: null,
              accuracy: null,
              address: 'Location unavailable'
            });
          },
          {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
          }
        );
      } else {
        resolve({
          latitude: null,
          longitude: null,
          accuracy: null,
          address: 'Geolocation not supported'
        });
      }
    });
  };

  const handleEmergencyClick = () => {
    setShowConfirm(true);
    setResult(null);
  };

  const handleConfirm = async () => {
    setSending(true);
    setResult(null);

    try {
      // Get location
      const locationData = await getLocation();
      setLocation(locationData);

      // Send emergency alert
      const response = await fetch('http://localhost:8000/api/emergency/alert/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          session_id: sessionId,
          location: locationData,
          crisis_context: crisisContext,
          user_name: userName,
          is_test: false
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to send emergency alert');
      }

      setResult({
        success: true,
        message: data.message,
        details: data
      });
    } catch (err) {
      setResult({
        success: false,
        message: err.message
      });
    } finally {
      setSending(false);
    }
  };

  const handleCancel = () => {
    setShowConfirm(false);
    setResult(null);
  };

  const handleClose = () => {
    setShowConfirm(false);
    setResult(null);
    setLocation(null);
  };

  return (
    <>
      {/* Emergency Button */}
      <button
        onClick={handleEmergencyClick}
        className="fixed bottom-6 right-6 bg-gradient-to-r from-red-500 to-red-600 text-white p-4 rounded-full shadow-2xl hover:from-red-600 hover:to-red-700 transition-all transform hover:scale-110 z-40 animate-pulse"
        title="Emergency Help"
      >
        <AlertCircle size={28} />
      </button>

      {/* Confirmation Modal */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full">
            {!result ? (
              <>
                {/* Confirmation Screen */}
                <div className="bg-gradient-to-r from-red-500 to-red-600 p-6 rounded-t-2xl">
                  <div className="flex items-center gap-3 text-white">
                    <AlertCircle size={32} />
                    <h2 className="text-2xl font-bold">Emergency Alert</h2>
                  </div>
                </div>

                <div className="p-6 space-y-4">
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <p className="text-yellow-800 font-medium mb-2">
                      Are you sure you need emergency help?
                    </p>
                    <p className="text-yellow-700 text-sm">
                      This will immediately notify all your emergency contacts with:
                    </p>
                    <ul className="mt-2 space-y-1 text-sm text-yellow-700">
                      <li className="flex items-center gap-2">
                        <MapPin size={14} />
                        Your current location
                      </li>
                      <li className="flex items-center gap-2">
                        <AlertCircle size={14} />
                        Your mental health status
                      </li>
                      <li className="flex items-center gap-2">
                        <Send size={14} />
                        Crisis helpline numbers
                      </li>
                    </ul>
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <p className="text-blue-800 text-sm font-medium mb-2">
                      🆘 Immediate Crisis Resources:
                    </p>
                    <div className="space-y-1 text-sm text-blue-700">
                      <p>• AASRA: <a href="tel:9820466726" className="font-semibold underline">9820466726</a></p>
                      <p>• Vandrevala: <a href="tel:18602662345" className="font-semibold underline">1860-2662-345</a></p>
                      <p>• iCall: <a href="tel:9152987821" className="font-semibold underline">9152987821</a></p>
                      <p>• NIMHANS: <a href="tel:08046110007" className="font-semibold underline">080-46110007</a></p>
                    </div>
                  </div>

                  <div className="flex gap-3 pt-2">
                    <button
                      onClick={handleConfirm}
                      disabled={sending}
                      className="flex-1 bg-gradient-to-r from-red-500 to-red-600 text-white py-3 rounded-lg font-semibold hover:from-red-600 hover:to-red-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      {sending ? (
                        <>
                          <Loader className="animate-spin" size={20} />
                          Sending Alert...
                        </>
                      ) : (
                        <>
                          <Send size={20} />
                          Yes, Send Alert
                        </>
                      )}
                    </button>
                    <button
                      onClick={handleCancel}
                      disabled={sending}
                      className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors disabled:opacity-50"
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                {/* Result Screen */}
                <div className={`p-6 rounded-t-2xl ${result.success ? 'bg-gradient-to-r from-green-500 to-green-600' : 'bg-gradient-to-r from-red-500 to-red-600'}`}>
                  <div className="flex items-center gap-3 text-white">
                    {result.success ? (
                      <CheckCircle size={32} />
                    ) : (
                      <XCircle size={32} />
                    )}
                    <h2 className="text-2xl font-bold">
                      {result.success ? 'Alert Sent!' : 'Alert Failed'}
                    </h2>
                  </div>
                </div>

                <div className="p-6 space-y-4">
                  <div className={`border rounded-lg p-4 ${result.success ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'}`}>
                    <p className={`font-medium ${result.success ? 'text-green-800' : 'text-red-800'}`}>
                      {result.message}
                    </p>
                    {result.success && result.details && (
                      <div className="mt-3 space-y-2 text-sm text-green-700">
                        <p>✅ Alerts sent: {result.details.alerts_sent}/{result.details.total_contacts}</p>
                        {result.details.delivery_status && result.details.delivery_status.map((status, idx) => (
                          <div key={idx} className="pl-4 border-l-2 border-green-300">
                            <p className="font-medium">{status.contact_name}</p>
                            <p className="text-xs">
                              {status.whatsapp_sent && '✓ WhatsApp'} 
                              {status.whatsapp_sent && status.sms_sent && ' • '}
                              {status.sms_sent && '✓ SMS'}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  {result.success && location && location.latitude && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <p className="text-blue-800 text-sm font-medium mb-2">
                        📍 Location Shared:
                      </p>
                      <p className="text-blue-700 text-xs">
                        Lat: {location.latitude.toFixed(6)}, Lng: {location.longitude.toFixed(6)}
                      </p>
                      <a
                        href={`https://maps.google.com/?q=${location.latitude},${location.longitude}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 text-sm underline mt-2 inline-block"
                      >
                        View on Google Maps
                      </a>
                    </div>
                  )}

                  <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                    <p className="text-purple-800 text-sm">
                      {result.success 
                        ? 'Your emergency contacts have been notified and should reach out to you soon. Please stay safe and consider calling a crisis helpline.'
                        : 'Please try calling a crisis helpline directly or contact your emergency contacts manually.'}
                    </p>
                  </div>

                  <button
                    onClick={handleClose}
                    className="w-full bg-gray-600 text-white py-3 rounded-lg font-semibold hover:bg-gray-700 transition-colors"
                  >
                    Close
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </>
  );
};

export default EmergencyAlertButton;

