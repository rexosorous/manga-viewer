@echo off
pyuic5 search_frame.ui -o search_frame.py
pyuic5 details_frame.ui -o details_frame.py
pyuic5 main_window.ui -o main_window.py
pyuic5 metadata_frame.ui -o metadata_frame.py
pyuic5 reader_window.ui -o reader_window.py
pyuic5 page_preview.ui -o page_preview.py
pyuic5 bookshelf_frame.ui -o bookshelf_frame.py