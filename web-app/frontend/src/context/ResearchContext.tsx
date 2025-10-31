import React, { createContext, useContext, useReducer } from 'react';
import type { ReactNode } from 'react';
import type { ResearchState, ResearchRequest, ResearchResult } from '../types';

type ResearchAction =
  | { type: 'START_RESEARCH' }
  | { type: 'RESEARCH_SUCCESS'; payload: ResearchResult }
  | { type: 'RESEARCH_ERROR'; payload: string }
  | { type: 'CLEAR_RESULTS' };

interface ResearchContextType {
  state: ResearchState;
  startResearch: (request: ResearchRequest) => Promise<void>;
  clearResults: () => void;
}

const initialState: ResearchState = {
  isLoading: false,
  result: null,
  error: null,
};

const researchReducer = (state: ResearchState, action: ResearchAction): ResearchState => {
  switch (action.type) {
    case 'START_RESEARCH':
      return { ...state, isLoading: true, error: null };
    case 'RESEARCH_SUCCESS':
      return { ...state, isLoading: false, result: action.payload, error: null };
    case 'RESEARCH_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'CLEAR_RESULTS':
      return { ...state, result: null, error: null };
    default:
      return state;
  }
};

const ResearchContext = createContext<ResearchContextType | undefined>(undefined);

export const ResearchProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(researchReducer, initialState);

  const startResearch = async (request: ResearchRequest) => {
    dispatch({ type: 'START_RESEARCH' });
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      
      // Step 1: Start the research
      const startResponse = await fetch(`${apiUrl}/api/research/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: request.query,
          report_type: request.reportType,
          prompt_type: 'general',
          automation_level: 'full'
        }),
      });

      if (!startResponse.ok) {
        throw new Error('Failed to start research');
      }

      const startResult = await startResponse.json();
      const sessionId = startResult.data.session_id;

      // Step 2: Poll for completion
      const pollForResult = async (): Promise<ResearchResult> => {
        while (true) {
          const statusResponse = await fetch(`${apiUrl}/api/research/${sessionId}/status`);
          if (!statusResponse.ok) {
            throw new Error('Failed to check research status');
          }

          const status = await statusResponse.json();
          
          if (status.status === 'completed') {
            // Get the final result
            const resultResponse = await fetch(`${apiUrl}/api/research/${sessionId}/result`);
            if (!resultResponse.ok) {
              throw new Error('Failed to get research result');
            }
            
            const result = await resultResponse.json();
            return {
              report: result.report_content,
              sources: result.sources || [],
              wordCount: result.report_content ? result.report_content.split(' ').length : 0,
              citations: result.citations || [],
              timestamp: result.completed_at || new Date().toISOString()
            };
          } else if (status.status === 'failed') {
            throw new Error('Research failed');
          }
          
          // Wait 2 seconds before polling again
          await new Promise(resolve => setTimeout(resolve, 2000));
        }
      };

      const result = await pollForResult();
      dispatch({ type: 'RESEARCH_SUCCESS', payload: result });
      
    } catch (error) {
      dispatch({ 
        type: 'RESEARCH_ERROR', 
        payload: error instanceof Error ? error.message : 'An unknown error occurred' 
      });
    }
  };

  const clearResults = () => {
    dispatch({ type: 'CLEAR_RESULTS' });
  };

  return (
    <ResearchContext.Provider value={{ state, startResearch, clearResults }}>
      {children}
    </ResearchContext.Provider>
  );
};

export const useResearch = () => {
  const context = useContext(ResearchContext);
  if (context === undefined) {
    throw new Error('useResearch must be used within a ResearchProvider');
  }
  return context;
};