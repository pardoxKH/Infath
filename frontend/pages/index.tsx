import Head from 'next/head';
import { useState } from 'react';
import PropertyForm, { PredictionResult } from '../components/PropertyForm';
import Image from 'next/image';

export default function Home() {
  const [result, setResult] = useState<PredictionResult | null>(null);

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>تقييم العقار | Infath</title>
        <meta name="description" content="تقييم العقارات في المملكة العربية السعودية" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <Image
                src="/infath-color-logo.svg"
                alt="Infath Logo"
                width={120}
                height={40}
                className="h-10 w-auto"
              />
            </div>
            <h1 className="text-2xl font-bold text-infath-primary font-arabic">تقييم العقار</h1>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-lg p-6 md:p-8">
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold text-gray-900 font-arabic mb-2">تقييم العقار</h2>
              <p className="text-gray-600 font-arabic">أدخل بيانات العقار للحصول على تقييم فوري</p>
            </div>
            <PropertyForm onResult={setResult} />
            {result && (
              <div className="mt-8 p-6 bg-infath-primary/5 rounded-xl border border-infath-primary/20">
                <h3 className="text-lg font-semibold text-infath-primary font-arabic mb-2 text-center">نتيجة التقييم</h3>
                <p className="text-3xl font-bold text-gray-900 font-arabic text-center">
                  {new Intl.NumberFormat('en-US', {
                    style: 'decimal',
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2
                  }).format(result.prediction)} ريال
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
} 