export interface AgentRequest {
  id: string;
  userId: string;
  action: string;
  parameters: Record<string, any>;
  timestamp: Date;
}

export interface AgentResponse {
  requestId: string;
  status: 'success' | 'error' | 'pending';
  result?: any;
  error?: ErrorDetail;
  timestamp: Date;
}

export interface AgentConfig {
  apiKey: string;
  baseUrl: string;
  timeout: number;
  retryAttempts: number;
}

interface ErrorDetail {
  code: string;
  message: string;
  details?: Record<string, any>;
  correlationId: string;
}
