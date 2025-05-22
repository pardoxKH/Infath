import { useState } from 'react';

export interface PredictionResult {
  prediction: number;
}

interface PropertyFormProps {
  onResult: (result: PredictionResult) => void;
}

const initialState = {
  Area: '1050',
  AssetLevelId: 'C',
  East_order: 'قطعة رقم 615',
  EvaluationAssetTypeName: 'Housing Land',
  Latitude: '24.32',
  LengthFromEast: '30.14',
  LengthFromNorth: '38.45',
  LengthFromSouth: '28.46',
  LengthFromWest: '30.13',
  Longitude: '39.25',
  NorthBorder: 'قطعة رقم بدون',
  PropAssetCityName: 'Madinah',
  PropAssetNeighborhoodName: 'العزيزية',
  PropAssetRegionName: 'Madinah',
  SouthBorder: 'قطعة رقم 162وشارع عرض 12 م',
  StreetWidth: '12',
  WestBorder: 'قطعة رقم 163'
};

type FormState = typeof initialState;

const fieldLabels: Record<keyof FormState, string> = {
  Area: 'المساحة (متر مربع)',
  AssetLevelId: 'مستوى العقار',
  East_order: 'الحد الشرقي',
  EvaluationAssetTypeName: 'نوع العقار',
  Latitude: 'خط العرض',
  LengthFromEast: 'الطول من الشرق (متر)',
  LengthFromNorth: 'الطول من الشمال (متر)',
  LengthFromSouth: 'الطول من الجنوب (متر)',
  LengthFromWest: 'الطول من الغرب (متر)',
  Longitude: 'خط الطول',
  NorthBorder: 'الحد الشمالي',
  PropAssetCityName: 'المدينة',
  PropAssetNeighborhoodName: 'الحي',
  PropAssetRegionName: 'المنطقة',
  SouthBorder: 'الحد الجنوبي',
  StreetWidth: 'عرض الشارع (متر)',
  WestBorder: 'الحد الغربي',
};

const regions = [
  "Riyadh",
  "Makkah",
  "Madinah",
  "Eastern Province",
  "Asir",
  "Tabuk",
  "Hail",
  "Northern Borders",
  "Jazan",
  "Najran",
  "Al Baha",
  "Al Jawf",
  "Al Qassim"
];

const cityRegionMapping: Record<string, string[]> = {
  "Asir": ["بيشه", "خميس مشيط", "ابها", "احد رفيده", "محايل", "ظهران الجنوب", "بلقرن", "تثليث", "طريب", "المضه", "العرين", "النماص", "سراة عبيده", "المجارده", "رجال المع", "الحرجة", "الربوعه", "الشعف", "الواديين", "بارق", "البرك", "الحريضة", "تنومة", "خيبر الجنوب", "يعرى", "الصبيخه", "القحمه", "بني عمرو", "تهامة باللسمر وبللحمر"],
  "Bahah": ["الباحة", "بلجرشي", "الحجرة", "العقيق", "المخواة", "قلوة", "القرى", "المندق"],
  "Eastern Province": ["الاحساء", "الدمام", "حفر الباطن", "الخبر", "القطيف", "الخفجي", "الجبيل", "ابقيق", "النعيرية", "العيون", "رأس تنوره", "السعيره"],
  "Hail": ["حائل", "بقعاء", "الشنان", "الروضة", "الاجفر", "الشملي", "الغزاله", "سميراء"],
  "Jawf": ["سكاكا", "القريات", "دومة الجندل", "طبرجل"],
  "Jizan": ["جيزان", "صبياء", "صامطة", "أبو عريش", "بيش", "ضمد", "أحد المسارحة", "فاراسان", "الشقيق", "الطوال", "العيدابي", "الموسم"],
  "Madinah": ["المدينة المنورة", "الحناكية", "المهد", "وادي الفرع", "السويرقيه", "الصويدره"],
  "Makkah": ["جده", "مكة المكرمة", "الطائف", "تربه", "القنفذه", "الليث", "رابغ", "رنيه", "الخرمة", "الجموم", "خليص", "أضم", "المويه", "القوز", "العرضيات", "المضيلف", "ثقيف", "حلى", "ميسان"],
  "Najran": ["نجران", "شرورة", "يدمة", "بدر الجنوب"],
  "Northern Borders": ["عرعر", "رفحاء", "طريف", "العويقيلة"],
  "Qassim": ["بريده", "رياض الخبراء", "عنيزه", "البكيريه", "الرس", "البدائع", "المذنب", "عيون الجواء", "القواره", "النبهانيه", "قصيباء", "الشماسيه", "عقلة الصقور", "الاسياح", "الدليميه", "قبه", "ضريه"],
  "Riyadh": ["الرياض", "حريملاء", "الخرج", "المزاحميه", "القويعيه", "ضرماء", "الدوادمي", "الافلاج", "المجمعه", "الدرعيه", "الزلفي", "الدلم", "ريمة", "حوطة بني تميم", "ثادق", "شقراء", "عفيف", "وادي الدواسر", "الرين", "ساجر", "السليل", "مرات", "الغاط", "حوطة سدير", "الارطاويه", "الجمش", "الحريق", "تمير", "نفي", "البجاديه", "العيينة", "جلاجل", "عرجاء"],
  "Tabuk": ["تبوك", "تيماء", "بئر بن هرماس", "ضباء"]
};

const assetTypes = [
  "Housing Land",
  "Commercial Land",
  "Raw Land",
  "Farming Land"
];

const assetLevels = ['A', 'B', 'C', 'D'];

const requiredFields: (keyof FormState)[] = [
  'Area',
  'AssetLevelId',
  'East_order',
  'EvaluationAssetTypeName',
  'Latitude',
  'LengthFromEast',
  'LengthFromNorth',
  'LengthFromSouth',
  'LengthFromWest',
  'Longitude',
  'NorthBorder',
  'PropAssetCityName',
  'PropAssetNeighborhoodName',
  'PropAssetRegionName',
  'SouthBorder',
  'StreetWidth',
  'WestBorder',
];

export default function PropertyForm({ onResult }: PropertyFormProps) {
  const [form, setForm] = useState<FormState>(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm((prev) => {
      const newForm = { ...prev, [name]: value };
      // Reset city when region changes
      if (name === 'PropAssetRegionName') {
        newForm.PropAssetCityName = '';
      }
      return newForm;
    });
  };

  const validateNumericField = (value: string, field: string): boolean => {
    const num = Number(value);
    if (isNaN(num)) return false;
    
    switch (field) {
      case 'Area':
      case 'StreetWidth':
        return num > 0;
      case 'LengthFromNorth':
      case 'LengthFromSouth':
      case 'LengthFromEast':
      case 'LengthFromWest':
        return num >= 0;
      case 'Latitude':
        return num >= -90 && num <= 90;
      case 'Longitude':
        return num >= -180 && num <= 180;
      default:
        return true;
    }
  };

  const validate = () => {
    // Check required fields
    for (const field of requiredFields) {
      if (!form[field]) {
        setError(`يرجى ملء حقل ${fieldLabels[field]}`);
        return false;
      }
    }

    // Validate numeric fields
    const numericFields = ['Area', 'LengthFromNorth', 'LengthFromSouth', 'LengthFromEast', 
                          'LengthFromWest', 'StreetWidth', 'Latitude', 'Longitude'];
    
    for (const field of numericFields) {
      if (!validateNumericField(form[field as keyof FormState], field)) {
        setError(`قيمة غير صالحة في حقل ${fieldLabels[field as keyof FormState]}`);
        return false;
      }
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!validate()) {
      return;
    }
    setLoading(true);
    try {
      const payload = {
        ...form,
        Area: Number(form.Area),
        Latitude: Number(form.Latitude),
        Longitude: Number(form.Longitude),
        LengthFromEast: Number(form.LengthFromEast),
        LengthFromNorth: Number(form.LengthFromNorth),
        LengthFromSouth: Number(form.LengthFromSouth),
        LengthFromWest: Number(form.LengthFromWest),
        StreetWidth: Number(form.StreetWidth),
      };
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error('فشل التقييم');
      const data = await res.json();
      onResult(data);
    } catch (err: any) {
      setError(err.message || 'حدث خطأ');
    } finally {
      setLoading(false);
    }
  };

  const renderField = (key: keyof FormState) => {
    const label = fieldLabels[key];
    const value = form[key];

    if (key === 'PropAssetRegionName') {
      return (
        <select
          id={key}
          name={key}
          className="border border-infath-primary/20 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-infath-primary/30 font-arabic text-right"
          value={value}
          onChange={handleChange}
          required
        >
          <option value="">اختر المنطقة</option>
          {regions.map(region => (
            <option key={region} value={region}>{region}</option>
          ))}
        </select>
      );
    }

    if (key === 'PropAssetCityName') {
      const cities = form.PropAssetRegionName ? cityRegionMapping[form.PropAssetRegionName] || [] : [];
      return (
        <select
          id={key}
          name={key}
          className="border border-infath-primary/20 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-infath-primary/30 font-arabic text-right"
          value={value}
          onChange={handleChange}
          required
          disabled={!form.PropAssetRegionName}
        >
          <option value="">اختر المدينة</option>
          {cities.map(city => (
            <option key={city} value={city}>{city}</option>
          ))}
        </select>
      );
    }

    if (key === 'EvaluationAssetTypeName') {
      return (
        <select
          id={key}
          name={key}
          className="border border-infath-primary/20 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-infath-primary/30 font-arabic text-right"
          value={value}
          onChange={handleChange}
          required
        >
          <option value="">اختر نوع العقار</option>
          {assetTypes.map(type => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
      );
    }

    if (key === 'AssetLevelId') {
      return (
        <select
          id={key}
          name={key}
          className="border border-infath-primary/20 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-infath-primary/30 font-arabic text-right"
          value={value}
          onChange={handleChange}
          required
        >
          <option value="">اختر مستوى العقار</option>
          {assetLevels.map(level => (
            <option key={level} value={level}>{level}</option>
          ))}
        </select>
      );
    }

    return (
      <input
        id={key}
        name={key}
        type={key.toLowerCase().includes('latitude') || key.toLowerCase().includes('longitude') || 
              key.toLowerCase().includes('length') || key === 'Area' || key === 'StreetWidth' ? 'number' : 'text'}
        step="any"
        className="border border-infath-primary/20 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-infath-primary/30 font-arabic text-right"
        value={value}
        onChange={handleChange}
        required
        placeholder={`أدخل ${label.toLowerCase()}`}
        min={key === 'Area' || key === 'StreetWidth' ? '0.01' : 
             key.toLowerCase().includes('length') ? '0' : undefined}
      />
    );
  };

  // Define the order of fields with logical grouping
  const fieldGroups: { title: string; fields: (keyof FormState)[] }[] = [
    {
      title: 'معلومات الموقع',
      fields: [
        'PropAssetRegionName',
        'PropAssetCityName',
        'PropAssetNeighborhoodName',
        'Latitude',
        'Longitude'
      ]
    },
    {
      title: 'معلومات العقار',
      fields: [
        'Area',
        'AssetLevelId',
        'EvaluationAssetTypeName',
        'StreetWidth'
      ]
    },
    {
      title: 'قياسات العقار',
      fields: [
        'LengthFromNorth',
        'LengthFromSouth',
        'LengthFromEast',
        'LengthFromWest'
      ]
    },
    {
      title: 'حدود العقار',
      fields: [
        'NorthBorder',
        'SouthBorder',
        'East_order',
        'WestBorder'
      ]
    }
  ];

  return (
    <form className="space-y-8" onSubmit={handleSubmit} dir="rtl">
      {fieldGroups.map((group, groupIndex) => (
        <div key={groupIndex} className="bg-white rounded-xl p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-infath-primary mb-6 font-arabic">{group.title}</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {group.fields.map((key) => (
              <div key={key} className="flex flex-col">
                <label htmlFor={key} className="font-medium mb-2 text-infath-primary font-arabic text-right">
                  {fieldLabels[key]} <span className="text-red-500">*</span>
                </label>
                {renderField(key)}
              </div>
            ))}
          </div>
        </div>
      ))}
      
      {error && (
        <div className="text-red-600 font-medium font-arabic bg-red-50 p-4 rounded-lg border border-red-200 text-right">
          {error}
        </div>
      )}
      
      <button
        type="submit"
        className="w-full py-4 px-6 bg-infath-primary text-white font-arabic text-lg font-semibold rounded-lg shadow-infath hover:bg-infath-dark transition disabled:opacity-50 disabled:cursor-not-allowed"
        disabled={loading}
      >
        {loading ? 'جاري التقييم...' : 'احصل على التقييم'}
      </button>
    </form>
  );
} 