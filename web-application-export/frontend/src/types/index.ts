export interface ResearchRequest {
  query: string;
  reportType: 'concise' | 'detailed';
  apiKeys: {
    gemini?: string;
    serper?: string;
  };
}

export interface ResearchResult {
  report: string;
  sources: string[];
  wordCount: number;
  citations: string[];
  timestamp: string;
}

export interface ResearchState {
  isLoading: boolean;
  result: ResearchResult | null;
  error: string | null;
}

export interface Citation {
  id: number;
  url: string;
  title: string;
}