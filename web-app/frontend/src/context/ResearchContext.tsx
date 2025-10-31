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
      const response = await fetch(`${apiUrl}/research`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error('Research request failed');
      }

      const result: ResearchResult = await response.json();
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