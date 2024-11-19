from PyPDF2 import PdfReader, PdfWriter

# 加载 PDF 文件
pdf_file = "/Users/adamlyu/PycharmProjects/AzureAISearchDemo/FAQ_Campuslife.pdf"
pdf_reader = PdfReader(pdf_file)

# 遍历每一页并保存为单页 PDF
for page_num in range(len(pdf_reader.pages)):
    pdf_writer = PdfWriter()
    pdf_writer.add_page(pdf_reader.pages[page_num])  # 添加单页

    # 保存单页 PDF 文件
    with open(f"output_page_{page_num + 1}.pdf", "wb") as output_pdf:
        pdf_writer.write(output_pdf)