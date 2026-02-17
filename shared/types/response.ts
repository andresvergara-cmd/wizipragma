export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: ErrorDetail;
  metadata?: ResponseMetadata;
}

export interface ErrorDetail {
  code: string;
  message: string;
  details?: Record<string, any>;
  correlationId: string;
}

export interface ResponseMetadata {
  timestamp: Date;
  version: string;
  correlationId: string;
}
