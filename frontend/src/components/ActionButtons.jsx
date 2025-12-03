import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, UserPlus } from 'lucide-react';

const ActionButtons = ({ showInHeader = false, isCrisis = false }) => {
  const navigate = useNavigate();

  const buttonClass = showInHeader
    ? "glass-effect px-4 py-2 rounded-lg flex items-center gap-2 hover:shadow-lg transition-all duration-300 text-sm"
    : "glass-effect px-6 py-4 rounded-xl flex items-center gap-3 hover:shadow-xl transition-all duration-300 transform hover:scale-105";

  const containerClass = showInHeader
    ? "flex items-center gap-2"
    : isCrisis
    ? "flex flex-col sm:flex-row gap-4 p-6 bg-gradient-to-r from-red-50 to-orange-50 rounded-xl border-2 border-red-200 animate-pulse-slow"
    : "flex flex-col sm:flex-row gap-4 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl";

  return (
    <div className={containerClass}>
      {!showInHeader && (
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            {isCrisis ? "🆘 Need Immediate Support?" : "💡 Helpful Resources"}
          </h3>
          <p className="text-sm text-gray-600">
            {isCrisis 
              ? "Access coping strategies and find professional help right away"
              : "Explore coping strategies and connect with professional therapists"}
          </p>
        </div>
      )}
      
      <div className="flex gap-3">
        <button
          onClick={() => navigate('/coping-strategies')}
          className={`${buttonClass} bg-gradient-to-r from-primary-500 to-secondary-500 text-white hover:from-primary-600 hover:to-secondary-600`}
          aria-label="View coping strategies"
        >
          <Heart className={showInHeader ? "w-4 h-4" : "w-5 h-5"} />
          <span className="font-medium">
            {showInHeader ? "Coping" : "Coping Strategies"}
          </span>
        </button>

        <button
          onClick={() => navigate('/find-therapist')}
          className={`${buttonClass} bg-gradient-to-r from-green-500 to-teal-500 text-white hover:from-green-600 hover:to-teal-600`}
          aria-label="Find a therapist"
        >
          <UserPlus className={showInHeader ? "w-4 h-4" : "w-5 h-5"} />
          <span className="font-medium">
            {showInHeader ? "Therapist" : "Find a Therapist"}
          </span>
        </button>
      </div>
    </div>
  );
};

export default ActionButtons;

