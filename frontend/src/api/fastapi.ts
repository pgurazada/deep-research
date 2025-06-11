import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const fetchAnswer = async (query: string) => {
    try {
        const response = await axios.post(`${API_URL}/answer`, { text: query });
        return response.data.data;
    } catch (error: any) {
        throw new Error(error?.response?.data?.detail || 'Error fetching answer');
    }
};

// Add this function if you implement a /history endpoint in your backend
export const fetchResearchHistory = async () => {
    try {
        const response = await axios.get(`${API_URL}/history`);
        return response.data.data;
    } catch (error: any) {
        throw new Error(error?.response?.data?.detail || 'Error fetching history');
    }
};