import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { api } from '../services/api';

const SampleBills = () => {
  const [samples, setSamples] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedImage, setSelectedImage] = useState(null);

  useEffect(() => {
    loadSampleBills();
  }, []);

  const loadSampleBills = async () => {
    try {
      setLoading(true);
      const response = await api.get('/sample-bills');
      setSamples(response.data.samples);
    } catch (error) {
      console.error('Error loading sample bills:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleImageClick = (sample) => {
    setSelectedImage(sample);
  };

  if (loading) {
    return (
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span className="text-2xl">💴</span>
            Sample Philippine Bills
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <Card className="w-full">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span className="text-2xl">💴</span>
            Sample Philippine Bills
            <Badge variant="secondary" className="ml-2">Dataset Images</Badge>
          </CardTitle>
          <p className="text-gray-600">
            These are authentic Philippine peso bills from our detection dataset
          </p>
        </CardHeader>
        <CardContent>
          {samples.length === 0 ? (
            <p className="text-center text-gray-500 py-8">No sample bills available</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {samples.map((sample, index) => (
                <div
                  key={index}
                  className="group cursor-pointer border-2 border-gray-200 rounded-lg overflow-hidden hover:border-blue-500 transition-all duration-300 hover:shadow-lg"
                  onClick={() => handleImageClick(sample)}
                >
                  <div className="aspect-[3/2] relative overflow-hidden bg-gray-100">
                    <img
                      src={`http://localhost:8000${sample.url}`}
                      alt={`Sample bill ${index + 1}`}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => {
                        e.target.src = '/placeholder-bill.jpg';
                      }}
                    />
                    <div className="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
                  </div>
                  <div className="p-3">
                    <p className="text-sm text-gray-600 truncate">
                      {sample.filename.replace(/\.jpg$/, '')}
                    </p>
                    <Badge variant="outline" className="mt-1 text-xs">
                      Authentic
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}
          
          <div className="mt-6 pt-4 border-t border-gray-200">
            <Button 
              onClick={loadSampleBills}
              variant="outline"
              className="w-full"
            >
              🔄 Load New Samples
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Modal for enlarged image view */}
      {selectedImage && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
          onClick={() => setSelectedImage(null)}
        >
          <div 
            className="bg-white rounded-lg max-w-4xl max-h-[90vh] overflow-auto"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-4 border-b border-gray-200 flex justify-between items-center">
              <h3 className="text-lg font-semibold">
                Philippine Peso Bill Sample
              </h3>
              <Button 
                variant="ghost"
                onClick={() => setSelectedImage(null)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </Button>
            </div>
            <div className="p-4">
              <img
                src={`http://localhost:8000${selectedImage.url}`}
                alt="Selected bill sample"
                className="w-full max-w-3xl mx-auto rounded-lg shadow-lg"
              />
              <div className="mt-4 text-center">
                <p className="text-sm text-gray-600">
                  {selectedImage.filename}
                </p>
                <Badge variant="outline" className="mt-2">
                  Dataset Image - Authentic Bill
                </Badge>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SampleBills;