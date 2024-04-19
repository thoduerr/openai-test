import unittest
from unittest.mock import patch, mock_open
from pathlib import Path

import pytest

from main import get_config, read_file_content, save_chat, load_or_initialize_chat, replace_reference_with_content, read_pdf_content
   
class TestReadFileContent(unittest.TestCase):
    
    @patch('pathlib.Path.read_text', return_value='file content')
    def test_read_file_content_success(self, mock_read_text):
        content = read_file_content(Path('/fake/path'))
        self.assertEqual(content, 'file content')

    @patch('pathlib.Path.read_text', side_effect=FileNotFoundError)
    def test_read_file_content_file_not_found(self, mock_read_text):
        with self.assertRaises(Exception):
            read_file_content(Path('/fake/path'))
    
    
# class TestReadPDFContent(unittest.TestCase):
    
#     @patch('pypdf.PageObject.extract_text', return_value='pdf file content')
#     def test_read_pdf_content_success(self, mock_read_text):
#         content = read_pdf_content(Path('/fake/path/test.pdf'))
#         self.assertEqual(content, 'pdf file content')

#     @patch('pypdf.PageObject.extract_text', side_effect=FileNotFoundError)
#     def test_read_pdf_content_file_not_found(self, mock_read_text):
#         with self.assertRaises(Exception):
#             read_pdf_content(Path('/fake/path'))

class TestGetConfig(unittest.TestCase):

    @patch('os.getenv', side_effect=lambda k, d=None: {'OPENAI_API_KEY': 'fake_key'}.get(k, d))
    def test_get_config(self, mock_getenv):
        config = get_config()
        self.assertEqual(config.api_key, 'fake_key')
        self.assertEqual(config.model, 'gpt-4-turbo')
        self.assertEqual(config.temperature, 0.3)
        self.assertEqual(config.max_tokens, 4096)
        self.assertEqual(config.topic, 'test')

class TestSaveChat(unittest.TestCase):
    
    @patch('pathlib.Path.write_text')
    def test_save_chat(self, mock_write_text):
        chat = [{'role': 'system', 'content': 'Welcome'}]
        save_chat(chat, Path('/fake/path'))
        mock_write_text.assert_called_once()
        
    @patch('pathlib.Path.write_text')
    def test_save_chat_error(self, mock_write_text):
        with pytest.raises(Exception, match=' E ERROR: Path'):
            save_chat('', None)


class TestLoadOrInitializeChat(unittest.TestCase):
    
    @patch('pathlib.Path.read_text', return_value='[{"role": "system", "content": "Welcome"}]')
    def test_load_chat_success(self, mock_read_text):
        chat = load_or_initialize_chat(Path('/fake/path'), "Hello", "user")
        self.assertEqual(len(chat), 2)
        self.assertEqual(chat[1]['role'], 'user')
        self.assertEqual(chat[1]['content'], 'Hello')
    
    @patch('main.read_file_content', return_value='hello system message')
    def test_load_chat_error(self, mock_read_text):
        chat = load_or_initialize_chat(Path('/fake/path'), "Hello", "user")
        self.assertEqual(len(chat), 2)
        self.assertEqual(chat[0]['role'], 'system')
        self.assertEqual(chat[0]['content'], 'hello system message')
        self.assertEqual(chat[1]['role'], 'user')
        self.assertEqual(chat[1]['content'], 'Hello')

class TestReplaceReferenceWithContent(unittest.TestCase):
    
    @patch('main.read_file_content', return_value='inserted content')
    def test_replace_reference_with_content(self, mock_read_file):
        input_string = "This is a reference to a file:example.txt and more text."
        expected_output = "This is a reference to a inserted content and more text."
        result = replace_reference_with_content(input_string)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()