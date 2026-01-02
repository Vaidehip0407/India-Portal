import { Link } from 'react-router-dom';
import { Zap, Flame, Droplets, Building, ArrowRight, ExternalLink, Shield } from 'lucide-react';

const Services = () => {
  const services = [
    {
      id: 'electricity',
      name: 'Electricity',
      nameHindi: 'बिजली',
      description: 'Name change application for electricity connection',
      icon: Zap,
      gradient: 'from-amber-400 to-orange-500',
      bgLight: 'bg-amber-50',
      borderColor: 'border-amber-200',
      providers: [
        { name: 'Torrent Power', url: 'https://connect.torrentpower.com' },
        { name: 'PGVCL', url: 'https://www.pgvcl.com' },
        { name: 'UGVCL', url: 'https://www.ugvcl.com' },
        { name: 'MGVCL', url: 'https://www.mgvcl.com' },
        { name: 'DGVCL', url: 'https://www.dgvcl.com' }
      ]
    },
    {
      id: 'gas',
      name: 'Gas',
      nameHindi: 'गैस',
      description: 'Name change application for gas connection',
      icon: Flame,
      gradient: 'from-red-400 to-rose-600',
      bgLight: 'bg-red-50',
      borderColor: 'border-red-200',
      providers: [
        { name: 'Adani Total Gas', url: 'https://www.adanigas.com' },
        { name: 'Gujarat Gas', url: 'https://iconnect.gujaratgas.com' },
        { name: 'Sabarmati Gas', url: 'https://www.sabarmatigas.com' }
      ]
    },
    {
      id: 'water',
      name: 'Water',
      nameHindi: 'पानी',
      description: 'Name change application for water connection',
      icon: Droplets,
      gradient: 'from-cyan-400 to-blue-500',
      bgLight: 'bg-cyan-50',
      borderColor: 'border-cyan-200',
      providers: [
        { name: 'AMC Water', url: 'https://ahmedabadcity.gov.in' },
        { name: 'SMC Water', url: 'https://www.suratmunicipal.gov.in' },
        { name: 'VMC Water', url: 'https://vmc.gov.in' },
        { name: 'GWSSB', url: 'https://gwssb.gujarat.gov.in' }
      ]
    },
    {
      id: 'property',
      name: 'Property',
      nameHindi: 'संपत्ति',
      description: 'Name change application for property records',
      icon: Building,
      gradient: 'from-emerald-400 to-green-600',
      bgLight: 'bg-emerald-50',
      borderColor: 'border-emerald-200',
      providers: [
        { name: 'AnyRoR Gujarat', url: 'https://anyror.gujarat.gov.in' },
        { name: 'e-Dhara', url: 'https://revenuedepartment.gujarat.gov.in' },
        { name: 'e-Nagar', url: 'https://enagar.gujarat.gov.in' },
        { name: 'iORA', url: 'https://iora.gujarat.gov.in' }
      ]
    }
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl flex items-center justify-center shadow-lg">
            <Shield className="w-7 h-7 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Name Change Services</h1>
            <p className="text-gray-500">गुजरात सरकारी सेवाएं • Apply for name change in your utility connections</p>
          </div>
        </div>
      </div>

      {/* Info Banner */}
      <div className="bg-gradient-to-r from-orange-100 to-green-100 border-l-4 border-orange-500 p-4 rounded-lg mb-6">
        <p className="text-sm text-gray-800">
          <strong>How it works:</strong> Select a service category below, fill in your details, and submit your application. You can track the status in "My Applications".
        </p>
      </div>

      {/* Services Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {services.map((service) => {
          const Icon = service.icon;
          return (
            <div 
              key={service.id}
              className="bg-white rounded-lg shadow-lg border-t-4 border-orange-500 overflow-hidden hover:shadow-2xl hover:scale-105 transition-all group"
            >
              {/* Header */}
              <div className={`bg-gradient-to-r ${service.gradient} p-6 relative`}>
                <div className="absolute top-0 right-0 w-20 h-20 opacity-10">
                  <div className="w-full h-full border-4 border-white rounded-full"></div>
                </div>
                <div className="flex items-center gap-4 relative z-10">
                  <div className="bg-white/25 p-3 rounded-lg border-2 border-white group-hover:bg-white/40 group-hover:scale-110 transition">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-white group-hover:translate-x-1 transition">{service.name}</h2>
                    <p className="text-white/90">{service.nameHindi}</p>
                  </div>
                </div>
              </div>

              {/* Content */}
              <div className="p-6 space-y-4">
                <p className="text-gray-700 text-sm">{service.description}</p>

                {/* Apply Button */}
                <Link
                  to={`/${service.id}`}
                  className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-orange-500 to-orange-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg hover:scale-105 transition-all"
                >
                  Apply Now <ArrowRight className="w-4 h-4" />
                </Link>

                {/* Official Portals */}
                <div className="border-t border-gray-200 pt-4">
                  <p className="text-xs font-semibold text-orange-700 uppercase tracking-wider mb-2">
                    Official Portals
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {service.providers.map((provider) => (
                      <a
                        key={provider.name}
                        href={provider.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-xs px-3 py-1.5 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 border border-orange-300 flex items-center gap-1 transition-all hover:scale-110"
                      >
                        {provider.name} <ExternalLink className="w-3 h-3" />
                      </a>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Help Section */}
      <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white border-t-4 border-orange-500">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-bold">Need Help?</h3>
            <p className="text-green-100 text-sm mt-1">
              Contact our support team for assistance
            </p>
          </div>
          <button className="px-6 py-3 bg-white text-green-600 rounded-lg font-semibold hover:shadow-lg transition-all hover:scale-105">
            Get Support
          </button>
        </div>
      </div>
    </div>
  );
};

export default Services;
