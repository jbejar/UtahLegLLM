from openai_processor.processor import OpenAIProcessor
from openai.types.chat import ChatCompletion
from openai.types.chat.chat_completion import Choice, ChatCompletionMessage
from openai_processor.processor import OpenAIProcessor
from unittest.mock import Mock, patch
import pytest

class TestProcessor:

    @pytest.fixture
    def mock_openai_client(self):
        with patch('openai.OpenAI') as mock_openai:
            mock_client = Mock()
            mock_openai.return_value = mock_client
            yield mock_client

    def test__analyze_content_api_error(self, mock_openai_client):
        """
        Test _analyze_content when API raises an error
        """
        processor = OpenAIProcessor()
        mock_openai_client.chat.completions.create.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="API Error"):
            processor._analyze_content("Test content")

    def test__analyze_content_empty_input(self, mock_openai_client):
        """
        Test _analyze_content with empty input
        """
        processor = OpenAIProcessor()
        with pytest.raises(ValueError, match="Content cannot be empty"):
            processor._analyze_content("")

    def test__analyze_content_empty_response(self, mock_openai_client):
        """
        Test _analyze_content when API returns empty response
        """
        processor = OpenAIProcessor()
        mock_response = ChatCompletion(id="1", choices=[], created=1, model="gpt-3.5-turbo", object="chat.completion")
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        with pytest.raises(IndexError):
            processor._analyze_content("Test content")

    def test__analyze_content_exceeds_max_length(self, mock_openai_client):
        """
        Test _analyze_content with input exceeding maximum length
        """
        processor = OpenAIProcessor()
        max_length = 4*7500  # Assuming a maximum length for the API
        long_content = "a" * (max_length + 1)
        with pytest.raises(ValueError, match="Content exceeds maximum length"):
            processor._analyze_content(long_content)

    def test__analyze_content_non_string_input(self, mock_openai_client):
        """
        Test _analyze_content with non-string input
        """
        processor = OpenAIProcessor()
        with pytest.raises(TypeError, match="Content must be a string"):
            processor._analyze_content(123)

    def test__analyze_content_for_real(self):
        """
        Test _analyze_content with None input
        """
        processor = OpenAIProcessor()
        result = processor._analyze_content("Please respond test to this input, Thank you!")
        assert len(result) > 100

    def test__analyze_content_unexpected_response(self, mock_openai_client):
        """
        Test _analyze_content when API returns unexpected response structure
        """
        processor = OpenAIProcessor()
        mock_openai_client.chat.completions.create.return_value = "Unexpected response"
        
        with pytest.raises(AttributeError):
            processor._analyze_content("Test content")

    def test_analyze_content_returns_expected_response(self):
        """
        Test that _analyze_content method returns the expected response from OpenAI API.
        """
        # Arrange
        processor = OpenAIProcessor()
        content = "Sample content for analysis"
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Analyzed content"))]

        with patch.object(processor.client.chat.completions, 'create', return_value=mock_response) as mock_create:
            # Act
            result = processor._analyze_content(content)

            # Assert
            mock_create.assert_called_once_with(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes text."},
                    {"role": "user", "content": f"Analyze this content: {content}"}
                ]
            )
            assert result == mock_response
            assert result.choices[0].message.content == "Analyzed content"