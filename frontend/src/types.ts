export interface PredictRequest {
  latitude: number
  longitude: number
  brightness: number
  scan: number
  track: number
  acq_time: number
  confidence: 'h' | 'l' | 'n'
  version: '2.0NRT'
  daynight: 'D' | 'N'
  fire_type: -1 | 0 | 2 | 3
  bright_t31: number
  frp: number
  observation_date: string
  observation_time: string
}

export interface RiskProbability {
  risk_level: string
  probability: number
}

export interface PredictResponse {
  predicted_risk: string
  confidence_score: number
  prediction_proba: RiskProbability[]

  fire_source: string
  fire_source_confidence: number

  fire_detected: boolean
  brightness_difference: number

  intensity: string
  intensity_message: string

  thermal_status: string
  thermal_message: string

  season: string

  latitude: number
  longitude: number
  brightness: number
  frp: number
  daynight: 'D' | 'N'
}

export interface FeatureImportance {
  feature: string
  importance: number
}

export interface MetaResponse {
  feature_columns: string[]
  risk_classes: string[]
  feature_importances: FeatureImportance[]
  fire_source_available: boolean
  performance: {
    model: string
    features: number
    test_samples: number
    accuracy: number
    verified: boolean
    caveat: string
  }
}

export type RiskLevel = 'Low' | 'Medium' | 'High' | string
