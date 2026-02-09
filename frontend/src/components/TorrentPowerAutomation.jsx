import { useState } from 'react';
import { Bot, CheckCircle, Play } from 'lucide-react';
import api from '../api/axios';

const TorrentPowerAutomation = ({ userData, onComplete, onClose }) => {
  const [automationStatus, setAutomationStatus] = useState('idle'); // idle, running, completed, failed
  const [result, setResult] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [realTimeStatus, setRealTimeStatus] = useState([]);
  const [progress, setProgress] = useState(0);
  const [fieldsCompleted, setFieldsCompleted] = useState(0);
  const totalFields = 5;

  const startClientAutomation = async () => {
    try {
      setAutomationStatus('running');
      setProgress(0);
      setFieldsCompleted(0);
      setStatusMessage('Initializing automation...');
      setRealTimeStatus(['⚡ Preparing to start automation...']);

      console.log('🔍 Debug - userData received:', userData);

      // Prepare data for backend
      const automationData = {
        city: userData.city || 'Ahmedabad',
        service_number: userData.serviceNumber || userData.service_number || '',
        t_number: userData.tNumber || userData.t_number || '',
        mobile: userData.mobile || '',
        email: userData.email || '',
        confirm_email: userData.confirmEmail || userData.email || ''
      };

      // Start polling for real-time status updates
      const statusPollInterval = setInterval(async () => {
        try {
          const statusResponse = await api.get('/torrent-automation/automation-status');
          const status = statusResponse.data;
          
          console.log('📊 Polling status:', status);
          
          if (status.success && status.status !== 'idle') {
            console.log(`✅ Status update: ${status.progress}% - ${status.message}`);
            
            // Update progress
            if (status.progress !== undefined) {
              setProgress(status.progress);
            }
            
            // Update message
            if (status.message) {
              setStatusMessage(status.message);
            }
            
            // Update fields completed
            if (status.fields_completed !== undefined) {
              setFieldsCompleted(status.fields_completed);
            }
            
            // Update real-time log
            if (status.logs && status.logs.length > 0) {
              const newLogs = status.logs.map(log => `${log.message}`);
              setRealTimeStatus(newLogs);
            }
            
            // Check if completed
            if (status.status === 'completed' || status.progress >= 100) {
              clearInterval(statusPollInterval);
              
              setTimeout(() => {
                setAutomationStatus('completed');
                setProgress(100);
                
                const result = {
                  success: true,
                  message: 'Application Submitted Successfully',
                  automation_type: 'automated',
                  details: 'Form automation completed successfully.',
                  fieldsCompleted: [
                    { field: 'City', status: 'completed', value: automationData.city },
                    { field: 'Service Number', status: 'completed', value: automationData.service_number },
                    { field: 'T Number', status: 'completed', value: automationData.t_number },
                    { field: 'Mobile Number', status: 'completed', value: automationData.mobile },
                    { field: 'Email', status: 'completed', value: automationData.email }
                  ],
                  notSubmitted: true
                };
                
                setResult(result);
              }, 1000);
            }
          }
        } catch (pollError) {
          console.error('⚠️ Status poll error:', pollError);
        }
      }, 500); // Poll every 500ms for real-time updates

      // Call backend API to start automation
      api.post('/torrent-automation/start-automation', automationData)
        .then(response => {
          console.log('✅ Automation started:', response.data);
          // Don't clear interval - let polling continue
        })
        .catch(error => {
          console.error('⚠️ Automation error:', error);
          clearInterval(statusPollInterval);
          
          setAutomationStatus('failed');
          setStatusMessage(`Failed: ${error.message}`);
          setResult({
            success: false,
            error: error.message,
            message: 'Automation failed'
          });
        });

    } catch (error) {
      console.error('❌ Automation error:', error);
      setAutomationStatus('failed');
      setStatusMessage(`Failed: ${error.message}`);
      setRealTimeStatus(prev => [...prev, `❌ Error: ${error.message}`]);
      setResult({
        success: false,
        error: error.message,
        message: 'Automation failed'
      });
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-t-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Bot className="w-6 h-6 text-white" />
              <h2 className="text-lg font-bold text-white">Torrent Power | Name Change Application</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:bg-white/20 p-2 rounded-full transition-colors text-2xl font-bold leading-none w-8 h-8 flex items-center justify-center"
              title="Close"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          
          {/* Progress Bar and Status - Only show when running */}
          {automationStatus === 'running' && (
            <div className="mb-6">
              {/* Progress Header */}
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-gray-800 text-lg">Automation Progress</h3>
                <span className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">{progress}%</span>
              </div>
              
              {/* Progress Bar with Gradient */}
              <div className="w-full bg-gray-200 rounded-full h-4 mb-6 overflow-hidden shadow-inner">
                <div 
                  className="h-full rounded-full transition-all duration-500 ease-out relative overflow-hidden"
                  style={{ 
                    width: `${progress}%`,
                    background: 'linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #3b82f6 100%)',
                    backgroundSize: '200% 100%',
                    animation: 'shimmer 2s infinite'
                  }}
                >
                  <div className="absolute inset-0 bg-white opacity-30 animate-pulse"></div>
                </div>
              </div>

              {/* Fields Counter with Icon */}
              <div className="text-center mb-6">
                <div className="inline-flex items-center gap-3 bg-gradient-to-r from-blue-50 to-purple-50 px-6 py-3 rounded-full border-2 border-blue-200">
                  <CheckCircle className="w-6 h-6 text-blue-600" />
                  <p className="text-xl font-bold text-gray-800">
                    {fieldsCompleted}/{totalFields} Fields Completed
                  </p>
                </div>
              </div>

              {/* Modern Loader with Current Status */}
              <div className="bg-gradient-to-br from-blue-50 via-purple-50 to-blue-50 border-2 border-blue-200 rounded-xl p-6 shadow-lg">
                <div className="flex items-center gap-4">
                  {/* Animated Loader */}
                  <div className="relative flex-shrink-0">
                    <div className="w-16 h-16 relative">
                      {/* Outer spinning ring */}
                      <div className="absolute inset-0 border-4 border-blue-200 rounded-full"></div>
                      <div className="absolute inset-0 border-4 border-transparent border-t-blue-600 border-r-purple-600 rounded-full animate-spin"></div>
                      {/* Inner pulsing circle */}
                      <div className="absolute inset-2 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full animate-pulse flex items-center justify-center">
                        <Bot className="w-6 h-6 text-white" />
                      </div>
                    </div>
                  </div>
                  
                  {/* Status Message */}
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-600 mb-1">Current Step</p>
                    <p className="font-bold text-blue-900 text-lg leading-tight">{statusMessage}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Success Result Display */}
          {result && result.success && automationStatus === 'completed' && (
            <div className="mb-4 bg-white border-2 border-gray-200 rounded-lg p-6 relative">
              {/* Close button on success modal */}
              <button
                onClick={onClose}
                className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors text-2xl font-bold leading-none w-8 h-8 flex items-center justify-center rounded-full hover:bg-gray-100"
                title="Close"
              >
                ✕
              </button>
              
              {/* Fields Completed */}
              <div className="space-y-2 mb-4 mt-2">
                {result.fieldsCompleted && result.fieldsCompleted.map((field, index) => (
                  <div key={index} className="flex items-center gap-3 text-sm">
                    <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0" />
                    <span className="text-gray-700">{field.field}</span>
                  </div>
                ))}
              </div>

              {/* Warning Message */}
              {result.notSubmitted && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="flex items-start gap-3 bg-red-50 p-4 rounded-lg">
                    <div className="flex-shrink-0 mt-1">
                      <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center">
                        <span className="text-white text-xl font-bold">✕</span>
                      </div>
                    </div>
                    <div>
                      <p className="font-semibold text-red-800 mb-1">
                        Application has not been submitted due to incorrect data.
                      </p>
                      <p className="text-sm text-red-700">
                        This is a demo with dummy data. The form was filled but not submitted to Torrent Power.
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* OK Button */}
              <div className="mt-6 flex justify-center">
                <button
                  onClick={onClose}
                  className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-colors"
                >
                  OK
                </button>
              </div>
            </div>
          )}

          {/* Error Display */}
          {result && !result.success && (
            <div className="mb-4 bg-red-50 border-2 border-red-200 rounded-xl p-6 relative">
              {/* Close button on error modal */}
              <button
                onClick={onClose}
                className="absolute top-2 right-2 text-red-400 hover:text-red-600 transition-colors text-xl font-bold leading-none w-6 h-6 flex items-center justify-center rounded-full hover:bg-red-100"
                title="Close"
              >
                ✕
              </button>
              
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0">
                  <div className="w-12 h-12 bg-red-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-2xl font-bold">✕</span>
                  </div>
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-red-800 text-lg mb-2">Automation Failed</h3>
                  <p className="text-red-700 mb-4">{result.message || result.error}</p>
                  
                  {result.error && result.error.includes("setup browser") && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mt-4">
                      <h4 className="font-semibold text-yellow-800 mb-2">💡 Possible Solutions:</h4>
                      <ul className="text-sm text-yellow-700 space-y-1 list-disc list-inside">
                        <li>Make sure Google Chrome is installed on your system</li>
                        <li>Try restarting the backend server</li>
                        <li>Check if ChromeDriver is compatible with your Chrome version</li>
                        <li>Contact support if the issue persists</li>
                      </ul>
                    </div>
                  )}
                  
                  <button
                    onClick={onClose}
                    className="mt-4 bg-red-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-red-700 transition-colors"
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Action Button - Only show when idle */}
          {automationStatus === 'idle' && (
            <div className="flex justify-center">
              <button
                onClick={startClientAutomation}
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-medium hover:from-blue-700 hover:to-purple-700 transition-colors flex items-center justify-center gap-2"
              >
                <Play className="w-5 h-5" />
                Start
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TorrentPowerAutomation;
