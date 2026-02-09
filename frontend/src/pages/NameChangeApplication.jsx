import { useState, useEffect } from 'react';
import { useParams, useSearchParams, Link } from 'react-router-dom';
import {
  Zap, Flame, Droplets, Building, ArrowLeft, Upload,
  User, Phone, Mail, MapPin, FileText, Calendar,
  AlertCircle, CheckCircle, Info, Sparkles, Play, Bot
} from 'lucide-react';
import axios from '../api/axios';
import TorrentPowerAutomation from '../components/TorrentPowerAutomation';

const NameChangeApplication = () => {
  const { serviceType } = useParams();
  const [searchParams] = useSearchParams();
  const providerId = searchParams.get('provider');

  const [formData, setFormData] = useState({
    // Torrent Power Specific Fields (only for torrent-power)
    city: 'Ahmedabad',
    serviceNumber: '',
    tNumber: '',
    mobile: '',
    email: '',
    confirmEmail: '',

    // Original fields for other providers
    currentName: '',
    newName: '',
    fatherName: '',
    motherName: '',
    dateOfBirth: '',
    gender: '',
    address: '',
    pincode: '',
    connectionNumber: '',
    connectionType: '',
    registeredAddress: '',
    identityProof: null,
    addressProof: null,
    nameChangeProof: null,
    connectionBill: null,
    applicationNumber: '',
    subdivisionCode: '',
    consumerCategory: '',
    loadSanctioned: '',
    aadhaarNumber: '',
    rationCardNumber: '',
    customerID: '',
    accountNumber: ''
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [showAutomation, setShowAutomation] = useState(false);
  const [automationCompleted, setAutomationCompleted] = useState(false);
  const [automationResult, setAutomationResult] = useState(null);

  const serviceConfig = {
    electricity: {
      name: 'Electricity',
      nameHindi: 'बिजली',
      icon: Zap,
      color: 'bg-yellow-500'
    },
    gas: {
      name: 'Gas',
      nameHindi: 'गैस',
      icon: Flame,
      color: 'bg-orange-500'
    },
    water: {
      name: 'Water',
      nameHindi: 'पानी',
      icon: Droplets,
      color: 'bg-blue-500'
    },
    property: {
      name: 'Property',
      nameHindi: 'संपत्ति',
      icon: Building,
      color: 'bg-green-500'
    }
  };

  // Provider configurations with specific requirements
  const providerConfig = {
    // Electricity Providers
    'pgvcl': {
      name: 'PGVCL',
      nameHindi: 'पीजीवीसीएल',
      type: 'Government',
      service: 'electricity',
      requiredFields: ['currentName', 'newName', 'connectionNumber', 'aadhaarNumber', 'mobile', 'email'],
      specificFields: ['subdivisionCode', 'consumerCategory'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '7-15 days',
      fees: 'As per GERC tariff'
    },
    'ugvcl': {
      name: 'UGVCL',
      nameHindi: 'यूजीवीसीएल',
      type: 'Government',
      service: 'electricity',
      requiredFields: ['currentName', 'newName', 'connectionNumber', 'aadhaarNumber', 'mobile'],
      specificFields: ['subdivisionCode', 'loadSanctioned'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '10-20 days',
      fees: 'Government prescribed fees'
    },
    'mgvcl': {
      name: 'MGVCL',
      nameHindi: 'एमजीवीसीएल',
      type: 'Government',
      service: 'electricity',
      requiredFields: ['currentName', 'newName', 'connectionNumber', 'aadhaarNumber', 'mobile'],
      specificFields: ['subdivisionCode', 'consumerCategory'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '7-15 days',
      fees: 'As per GERC tariff'
    },
    'dgvcl': {
      name: 'DGVCL',
      nameHindi: 'डीजीवीसीएल',
      type: 'Government',
      service: 'electricity',
      requiredFields: ['currentName', 'newName', 'connectionNumber', 'aadhaarNumber', 'mobile'],
      specificFields: ['subdivisionCode', 'consumerCategory'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '7-15 days',
      fees: 'Government prescribed fees'
    },
    'torrent-power': {
      name: 'Torrent Power',
      nameHindi: 'टॉरेंट पावर',
      type: 'Private',
      service: 'electricity',
      requiredFields: ['serviceNumber', 'tNumber', 'mobile', 'email', 'confirmEmail'],
      specificFields: ['city'],
      documents: [], // No documents required for online application
      processingTime: '5-10 days',
      fees: 'Rs. 100 + taxes',
      aiSupported: true,
      portalUrl: 'https://connect.torrentpower.com/tplcp/application/namechangerequest'
    },

    // Gas Providers
    'gujarat-gas': {
      name: 'Gujarat Gas Ltd',
      nameHindi: 'गुजरात गैस लिमिटेड',
      type: 'Government',
      service: 'gas',
      requiredFields: ['currentName', 'newName', 'connectionNumber', 'aadhaarNumber', 'mobile'],
      specificFields: ['consumerCategory', 'registeredAddress'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '10-20 days',
      fees: 'Government prescribed fees'
    },
    'adani-gas': {
      name: 'Adani Total Gas Ltd',
      nameHindi: 'अदानी टोटल गैस लिमिटेड',
      type: 'Private',
      service: 'gas',
      requiredFields: ['currentName', 'newName', 'customerID', 'mobile', 'email'],
      specificFields: ['accountNumber', 'connectionType'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '3-7 days',
      fees: 'Rs. 200 + taxes'
    },

    // Water Providers
    'amc-water': {
      name: 'AMC Water',
      nameHindi: 'एएमसी जल विभाग',
      type: 'Government',
      service: 'water',
      requiredFields: ['currentName', 'newName', 'connectionNumber', 'aadhaarNumber', 'mobile'],
      specificFields: ['wardNumber', 'propertyNumber'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'connectionBill'],
      processingTime: '15-30 days',
      fees: 'Municipal prescribed fees'
    },

    // Property Providers
    'anyror': {
      name: 'AnyRoR (Revenue Dept)',
      nameHindi: 'एनीआरओआर (राजस्व विभाग)',
      type: 'Government',
      service: 'property',
      requiredFields: ['currentName', 'newName', 'aadhaarNumber', 'mobile', 'fatherName'],
      specificFields: ['surveyNumber', 'villageCode', 'talukaCode'],
      documents: ['identityProof', 'addressProof', 'nameChangeProof', 'propertyDocuments'],
      processingTime: '30-60 days',
      fees: 'Revenue department fees'
    }
  };

  const provider = providerConfig[providerId];
  const service = serviceConfig[serviceType];
  const Icon = service?.icon;

  if (!provider || !service) {
    return <div>Provider or service not found</div>;
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const handleFileChange = (e) => {
    const { name, files } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: files[0]
    }));
  };

  const validateForm = () => {
    const newErrors = {};

    if (providerId === 'torrent-power') {
      // Torrent Power specific validation
      const requiredFields = ['serviceNumber', 'tNumber', 'mobile', 'email', 'confirmEmail'];

      requiredFields.forEach(field => {
        if (!formData[field]) {
          newErrors[field] = 'This field is required';
        }
      });

      // Email confirmation validation
      if (formData.email && formData.confirmEmail && formData.email !== formData.confirmEmail) {
        newErrors.confirmEmail = 'Email addresses do not match';
      }
    } else {
      // Original validation for other providers
      provider.requiredFields.forEach(field => {
        if (!formData[field]) {
          newErrors[field] = 'This field is required';
        }
      });

      provider.documents.forEach(doc => {
        if (!formData[doc]) {
          newErrors[doc] = 'This document is required';
        }
      });
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    // Check if this is Torrent Power with AI automation
    if (providerId === 'torrent-power' && provider.aiSupported) {
      setShowAutomation(true);
      return;
    }

    // Traditional submission for other providers
    setLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 2000));

      alert(`Application submitted successfully for ${provider.name}! You will receive a confirmation email shortly.`);

      // Reset form or redirect
      // navigate('/applications');

    } catch (error) {
      alert('Error submitting application. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAutomationComplete = (result) => {
    console.log('Automation completed:', result);
    setAutomationResult(result);
    setAutomationCompleted(true);
    setShowAutomation(false);
    
    if (result.success) {
      // Show success message
      setTimeout(() => {
        alert(`🎉 Application Submitted Successfully!\n\nYour name change request has been submitted to Torrent Power.\n\n✅ What happened:\n• Chrome browser opened automatically\n• Form was filled with your data\n• Application was submitted successfully\n\n📧 Next Steps:\n• You will receive a confirmation email shortly\n• Track your application on Torrent Power portal\n• Keep your reference number safe`);
      }, 500);
    } else {
      alert(`❌ Automation Failed!\n\n${result.error || result.message}\n\nPlease try the manual option or contact support.`);
    }
  };

  const handleCloseAutomation = () => {
    setShowAutomation(false);
  };

  const handleAutoFill = async () => {
    // 1. Prepare data mapping
    const dataToFill = {
      city: formData.city,
      service_number: formData.serviceNumber,
      transaction_number: formData.tNumber,
      mobile: formData.mobile,
      email: formData.email,
      old_name: formData.currentName // Mapping if available, though not main
    };

    // 2. Call Backend API for Live Automation
    setLoading(true);
    try {
      alert('🚀 Starting Live Automation...\n\nA browser window will open shortly. Please watch the process and manually log in if required.');

      await axios.post('/api/torrent-power/start-live-fill', {
        form_data: dataToFill
      });

      // Note: The backend returns when automation is "done" or "started". 
      // Our backend implementation currently waits for fill.
      // Once returned, we can notify user.
      alert('✅ Form Auto-filled Successfully!\n\nPlease review the data in the opened browser window and submit the form.');

    } catch (error) {
      console.error('Automation failed:', error);
      alert(`❌ Automation Failed: ${error.response?.data?.detail?.message || error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const renderField = (fieldName, label, type = 'text', required = false) => {
    const isRequired = provider.requiredFields.includes(fieldName) || required;

    return (
      <div key={fieldName}>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          {label} {isRequired && <span className="text-red-500">*</span>}
        </label>
        <input
          type={type}
          name={fieldName}
          value={formData[fieldName]}
          onChange={handleInputChange}
          className={`w-full px-4 py-3 border rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none transition-colors ${errors[fieldName] ? 'border-red-500' : 'border-gray-300'
            }`}
          placeholder={`Enter ${label.toLowerCase()}`}
        />
        {errors[fieldName] && (
          <p className="text-red-500 text-xs mt-1">{errors[fieldName]}</p>
        )}
      </div>
    );
  };

  const renderFileUpload = (fieldName, label, accept = '.pdf,.jpg,.jpeg,.png') => {
    const isRequired = provider.documents.includes(fieldName);

    return (
      <div key={fieldName}>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          {label} {isRequired && <span className="text-red-500">*</span>}
        </label>
        <div className={`border-2 border-dashed rounded-lg p-4 text-center ${errors[fieldName] ? 'border-red-500' : 'border-gray-300'
          }`}>
          <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
          <input
            type="file"
            name={fieldName}
            onChange={handleFileChange}
            accept={accept}
            className="hidden"
            id={fieldName}
          />
          <label
            htmlFor={fieldName}
            className="cursor-pointer text-blue-600 hover:text-blue-700 font-medium"
          >
            Click to upload {label.toLowerCase()}
          </label>
          <p className="text-xs text-gray-500 mt-1">PDF, JPG, PNG (Max 5MB)</p>
          {formData[fieldName] && (
            <p className="text-green-600 text-sm mt-2">✓ {formData[fieldName].name}</p>
          )}
        </div>
        {errors[fieldName] && (
          <p className="text-red-500 text-xs mt-1">{errors[fieldName]}</p>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Success Banner - Shows after automation completes */}
      {automationCompleted && automationResult?.success && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-6 mb-6">
          <div className="flex items-start gap-4">
            <CheckCircle className="w-8 h-8 text-green-600 mt-1" />
            <div className="flex-1">
              <h3 className="text-xl font-bold text-green-800 mb-2">🎉 Application Submitted Successfully!</h3>
              <p className="text-green-700 mb-4">
                Your name change request has been successfully submitted to Torrent Power through our AI automation system.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="bg-white rounded-lg p-4">
                  <h4 className="font-semibold text-green-800 mb-2">✅ Completed Actions:</h4>
                  <ul className="text-sm text-green-700 space-y-1">
                    <li>• Chrome browser opened automatically</li>
                    <li>• Navigated to Torrent Power website</li>
                    <li>• Form fields filled with your data</li>
                    <li>• Application submitted successfully</li>
                  </ul>
                </div>
                
                <div className="bg-blue-50 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-800 mb-2">📋 What's Next:</h4>
                  <ul className="text-sm text-blue-700 space-y-1">
                    <li>• Check your email for confirmation</li>
                    <li>• Track status on Torrent Power portal</li>
                    <li>• Processing time: {provider.processingTime}</li>
                    <li>• Keep your reference number safe</li>
                  </ul>
                </div>
              </div>

              {automationResult.total_filled && (
                <div className="bg-green-100 rounded-lg p-3">
                  <p className="text-sm text-green-800">
                    📊 <strong>Automation Stats:</strong> {automationResult.total_filled}/{automationResult.total_fields || 6} fields filled successfully
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Error Banner - Shows if automation fails */}
      {automationCompleted && automationResult && !automationResult.success && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-6">
          <div className="flex items-start gap-4">
            <AlertCircle className="w-8 h-8 text-red-600 mt-1" />
            <div className="flex-1">
              <h3 className="text-xl font-bold text-red-800 mb-2">❌ Automation Failed</h3>
              <p className="text-red-700 mb-4">
                {automationResult.message || automationResult.error || 'The automation process encountered an error.'}
              </p>
              
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="font-semibold text-yellow-800 mb-2">💡 Alternative Options:</h4>
                <ul className="text-sm text-yellow-700 space-y-1">
                  <li>• Try the automation again</li>
                  <li>• Use the "Open Manually" option</li>
                  <li>• Contact Torrent Power directly</li>
                  <li>• Visit their office for assistance</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-200">
        <div className="flex items-center gap-4">
          <Link
            to={`/service-providers/${serviceType}/name-change`}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5 text-gray-600" />
          </Link>
          <div className={`w-16 h-16 ${service.color} rounded-xl flex items-center justify-center`}>
            <Icon className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-gray-800">{service.name} Name Change Application</h1>
            <p className="text-gray-600 text-lg">{service.nameHindi} नाम परिवर्तन आवेदन</p>
            <p className="text-gray-500 text-sm mt-1">Provider: {provider.name} ({provider.type})</p>
          </div>
        </div>
      </div>

      {/* Provider Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <div className="flex items-start gap-4">
          <Info className="w-6 h-6 text-blue-600 mt-1" />
          <div>
            <h3 className="font-bold text-blue-900 mb-2">Application Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <span className="font-medium text-blue-800">Processing Time:</span>
                <p className="text-blue-700">{provider.processingTime}</p>
              </div>
              <div>
                <span className="font-medium text-blue-800">Application Fees:</span>
                <p className="text-blue-700">{provider.fees}</p>
              </div>
              <div>
                <span className="font-medium text-blue-800">Provider Type:</span>
                <p className="text-blue-700">{provider.type}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Application Form */}
      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm p-8 border border-gray-200">
        <h2 className="text-2xl font-bold text-gray-800 mb-8">Application Form</h2>

        {/* Torrent Power Specific Fields - Only for Torrent Power */}
        {providerId === 'torrent-power' ? (
          <div className="mb-8">
            <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Torrent Power Application Details
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

              {/* City Selection */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  City <span className="text-red-500">*</span>
                </label>
                <select
                  name="city"
                  value={formData.city || 'Ahmedabad'}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none"
                >
                  <option value="Ahmedabad">Ahmedabad</option>
                  <option value="Surat">Surat</option>
                  <option value="Gandhinagar">Gandhinagar</option>
                  <option value="Bhavnagar">Bhavnagar</option>
                </select>
              </div>

              {/* Service Number */}
              {renderField('serviceNumber', 'Service Number', 'text', true)}

              {/* T No (Transaction/Token Number) */}
              {renderField('tNumber', 'T No (Transaction Number)', 'text', true)}

              {/* Mobile Number */}
              {renderField('mobile', 'Mobile Number', 'tel', true)}

              {/* Email */}
              {renderField('email', 'Email Address', 'email', true)}

              {/* Confirm Email */}
              {renderField('confirmEmail', 'Confirm Email Address', 'email', true)}
            </div>
          </div>
        ) : (
          // Original form for all other providers
          <>
            {/* Personal Information */}
            <div className="mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <User className="w-5 h-5" />
                Personal Information
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {renderField('currentName', 'Current Name (as per connection)')}
                {renderField('newName', 'New Name (as per documents)')}
                {renderField('fatherName', "Father's Name")}
                {renderField('motherName', "Mother's Name")}
                {renderField('dateOfBirth', 'Date of Birth', 'date')}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">
                    Gender <span className="text-red-500">*</span>
                  </label>
                  <select
                    name="gender"
                    value={formData.gender}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-100 outline-none"
                  >
                    <option value="">Select Gender</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Contact Information */}
            <div className="mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Phone className="w-5 h-5" />
                Contact Information
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {renderField('mobile', 'Mobile Number', 'tel')}
                {renderField('email', 'Email Address', 'email')}
                {renderField('address', 'Current Address')}
                {renderField('pincode', 'PIN Code')}
              </div>
            </div>

            {/* Connection Details */}
            <div className="mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Connection Details
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {renderField('connectionNumber', 'Connection/Consumer Number')}
                {renderField('registeredAddress', 'Registered Address')}

                {/* Provider Specific Fields */}
                {provider.type === 'Government' && (
                  <>
                    {renderField('aadhaarNumber', 'Aadhaar Number')}
                    {renderField('rationCardNumber', 'Ration Card Number')}
                  </>
                )}

                {provider.type === 'Private' && provider.name !== 'Torrent Power' && (
                  <>
                    {renderField('customerID', 'Customer ID')}
                    {renderField('accountNumber', 'Account Number')}
                  </>
                )}

                {/* Service Specific Fields */}
                {provider.specificFields.includes('subdivisionCode') &&
                  renderField('subdivisionCode', 'Subdivision Code')}
                {provider.specificFields.includes('consumerCategory') &&
                  renderField('consumerCategory', 'Consumer Category')}
                {provider.specificFields.includes('loadSanctioned') &&
                  renderField('loadSanctioned', 'Load Sanctioned (KW)')}
                {provider.specificFields.includes('wardNumber') &&
                  renderField('wardNumber', 'Ward Number')}
                {provider.specificFields.includes('propertyNumber') &&
                  renderField('propertyNumber', 'Property Number')}
                {provider.specificFields.includes('surveyNumber') &&
                  renderField('surveyNumber', 'Survey Number')}
              </div>
            </div>

            {/* Document Upload */}
            <div className="mb-8">
              <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Required Documents
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {provider.documents.includes('identityProof') &&
                  renderFileUpload('identityProof', 'Identity Proof (Aadhaar/PAN/Passport)')}
                {provider.documents.includes('addressProof') &&
                  renderFileUpload('addressProof', 'Address Proof')}
                {provider.documents.includes('nameChangeProof') &&
                  renderFileUpload('nameChangeProof', 'Name Change Proof (Marriage Certificate/Gazette/Affidavit)')}
                {provider.documents.includes('connectionBill') &&
                  renderFileUpload('connectionBill', 'Latest Connection Bill')}
                {provider.documents.includes('propertyDocuments') &&
                  renderFileUpload('propertyDocuments', 'Property Documents')}
              </div>
            </div>
          </>
        )}

        {/* Submit or Auto-Fill Button */}
        <div className="flex items-center justify-between pt-6 border-t border-gray-200">
          <Link
            to={`/service-providers/${serviceType}/name-change`}
            className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            Back to Providers
          </Link>

          <div className="flex items-center gap-4">
            {providerId === 'torrent-power' && provider.aiSupported ? (
              <button
                type="submit"
                disabled={loading}
                className="px-8 py-3 rounded-lg font-bold transition-all duration-300 flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
              >
                <Play className="w-5 h-5" />
                Start
              </button>
            ) : (
              <button
                type="submit"
                disabled={loading}
                className="px-8 py-3 rounded-lg font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 bg-blue-600 text-white hover:bg-blue-700"
              >
                {loading ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Submitting...
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-5 h-5" />
                    Submit Application
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </form>

      {/* Torrent Power Automation Modal */}
      {showAutomation && (
        <TorrentPowerAutomation
          userData={formData}
          onComplete={handleAutomationComplete}
          onClose={handleCloseAutomation}
        />
      )}
    </div>
  );
};

export default NameChangeApplication;