import axios from 'axios';

const API_URL = process.env.EXPO_PUBLIC_API_URL;

const api = axios.create({
  baseURL: API_URL,
  timeout: 15000, // 15 seconds timeout
});

export interface FeedbackData {
  type: 'bad_response' | 'good_response' | 'general';
  message_text?: string; // The content of the message being reported
  message_id?: string; // The ID of the message
  contact_id: string; // Add contact_id field
  additional_notes?: string;
  category?: string; // e.g., 'irrelevant', 'incorrect', 'helpful'
}

export const submitFeedback = async (feedbackData: FeedbackData): Promise<any> => {
  try {
    const response = await api.post('/feedback', feedbackData);
    console.log('Feedback submitted:', response.data);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      console.error('Error submitting feedback:', {
        message: error.message,
        status: error.response?.status,
        data: error.response?.data,
      });
    } else {
      console.error('Error submitting feedback:', error);
    }
    throw error;
  }
};
