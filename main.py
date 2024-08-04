from fastapi import FastAPI

app = FastAPI()



"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import os
import time

import google.generativeai as genai

import requests


genai.configure(api_key="AIzaSyCbhcCCaoX7JdOlyh_-S87-c86IuPWdmf4")




def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """

  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

def wait_for_files_active(files):
  """Waits for the given files to be active.

  Some files uploaded to the Gemini API need to be processed before they can be
  used as prompt inputs. The status can be seen by querying the file's "state"
  field.

  This implementation uses a simple blocking polling loop. Production code
  should probably employ a more sophisticated approach.
  """
  print("Waiting for file processing...")
  for name in (file.name for file in files):
    file = genai.get_file(name)
    while file.state.name == "PROCESSING":
      print(".", end="", flush=True)
      time.sleep(10)
      file = genai.get_file(name)
    if file.state.name != "ACTIVE":
      raise Exception(f"File {file.name} failed to process")
  print("...all files ready")
  print()

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-exp-0801",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

# TODO Make these files available on the local file system
# You may need to update the file paths
files = [

]

videos = [
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722732230/gemini/s88ebzwrf6n1l9n8mrea.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722732230/gemini/s88ebzwrf6n1l9n8mrea.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722735877/gemini/ccmwxmlixonqxwkdajts.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722735877/gemini/ccmwxmlixonqxwkdajts.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722735958/gemini/sdns0piksmh1q0wwfju8.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736019/gemini/lj2yrccxrlcgwbxvlhui.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736089/gemini/wv8zh4laqhypu3qarjuu.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736180/gemini/pyv2ask6fnq2pluqvj1b.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736180/gemini/pyv2ask6fnq2pluqvj1b.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736308/gemini/al1yjwfdsbgngomivdje.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722735877/gemini/ccmwxmlixonqxwkdajts.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736391/gemini/gwysoqkbai5d8mctvqvu.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736449/gemini/bvkd9ujmek1lbfgo6rt6.mp4",
    "https://res.cloudinary.com/dqneghcme/video/upload/v1722736391/gemini/gwysoqkbai5d8mctvqvu.mp4",
]


for video in videos:
  response = requests.get(video)
  filename = video.split("/")[-1]
  with open(filename, "wb") as f:
    f.write(response.content)

  files.append(upload_to_gemini(filename, mime_type="video/mp4"))

# Some files have a processing delay. Wait for them to be ready.
wait_for_files_active(files)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        files[0],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[1],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[2],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[3],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[4],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[5],
      ],
    },
    {
      "role": "user",
      "parts": [
        files[6],
      ],
    },
    {
      "role": "user",
      "parts": [
        "Phan tich cac video sau",
      ],
    },
  ]
)

response = chat_session.send_message("Phan tich ki hon di")

@app.get("/")
def CheckDeepfake(video_path_cdn: str):

  response = requests.get(video_path_cdn)
  filename = video_path_cdn.split("/")[-1]
  with open(filename, "wb") as f:
    f.write(response.content)

  video_up = upload_to_gemini(filename, mime_type="video/mp4")

  file = genai.get_file(video_up.name)
  while file.state.name == "PROCESSING":
    print(".", end="", flush=True)
    time.sleep(10)
    file = genai.get_file(video_up.name)
  if file.state.name != "ACTIVE":
    raise Exception(f"File {file.name} failed to process")
  print("...all files ready")

  chat_session = model.start_chat(
    history=[
      {
        "role": "user",
        "parts": [
          "Giả sự bạn là một chuyên gia trong lĩnh vực phát hiện deepfake",
        ],
      },
      {
        "role": "model",
        "parts": [
          "## Tôi là chuyên gia phát hiện deepfake, và đây là những gì tôi có thể làm:\n\n**Kiến thức chuyên môn:**\n\n* **Hiểu biết sâu rộng về công nghệ deepfake:** Tôi am hiểu các thuật toán tạo deepfake, từ các kỹ thuật truyền thống như GANs và Autoencoders đến các kỹ thuật mới nổi như Diffusion Models.\n* **Nhận biết các dấu hiệu của deepfake:** Tôi có thể phân biệt deepfake từ video thật dựa trên các tín hiệu thị giác, âm thanh, và hành vi bất thường.\n* **Sử dụng công cụ và kỹ thuật phát hiện:** Tôi thành thạo các công cụ và kỹ thuật phát hiện deepfake, bao gồm cả các kỹ thuật xử lý tín hiệu, học máy và phân tích hành vi.\n* **Cập nhật kiến thức liên tục:** Tôi luôn theo sát các xu hướng mới nhất trong lĩnh vực phát hiện deepfake và cập nhật kiến thức để đối phó với những kỹ thuật deepfake ngày càng tinh vi.\n\n**Kỹ năng chuyên nghiệp:**\n\n* **Phân tích video và âm thanh:** Tôi có thể phân tích video và âm thanh để tìm kiếm dấu hiệu của deepfake.\n* **Kiểm tra tính xác thực:** Tôi có thể xác minh tính xác thực của video và âm thanh dựa trên các kỹ thuật chuyên môn.\n* **Báo cáo và tư vấn:** Tôi có thể cung cấp báo cáo về kết quả phân tích và tư vấn cho các khách hàng về cách bảo vệ mình khỏi deepfake.\n* **Hỗ trợ đào tạo:** Tôi có thể hỗ trợ đào tạo cho các cá nhân và tổ chức về cách nhận biết và phòng chống deepfake.\n\n**Ứng dụng thực tế:**\n\n* **Kiểm tra tin tức giả mạo:** Tôi có thể xác minh tính xác thực của các video và âm thanh được sử dụng trong tin tức để phát hiện tin tức giả mạo.\n* **Bảo vệ danh tính cá nhân:** Tôi có thể giúp người dùng bảo vệ danh tính của mình khỏi bị giả mạo bằng deepfake.\n* **Giảm thiểu thiệt hại:** Tôi có thể giúp các tổ chức phát hiện và ngăn chặn việc sử dụng deepfake để gây thiệt hại về tài chính hoặc danh tiếng.\n* **Nâng cao nhận thức về deepfake:** Tôi có thể góp phần nâng cao nhận thức về deepfake và các nguy cơ tiềm ẩn của nó trong xã hội.\n\n**Cam kết:**\n\nLà chuyên gia trong lĩnh vực phát hiện deepfake, tôi cam kết sử dụng kiến thức và kỹ năng của mình để góp phần bảo vệ xã hội khỏi các tác động tiêu cực của deepfake. Tôi luôn cập nhật kiến thức mới nhất và nỗ lực không ngừng để phát triển các kỹ thuật phát hiện deepfake hiệu quả hơn.\n\n**Lưu ý:** Mặc dù deepfake là một vấn đề nghiêm trọng, nhưng việc phát hiện và ngăn chặn nó đòi hỏi sự hợp tác của nhiều bên, từ các chuyên gia đến công chúng. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[0],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video sau là của deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Tôi cần xem video để xác định liệu đó là deepfake hay người thật. Xin bạn cung cấp link video. \n\nĐể phân tích, tôi sẽ quan sát các dấu hiệu sau:\n\n* **Sự bất thường về chuyển động:** Các chuyển động môi, mắt và cơ mặt có tự nhiên không?\n* **Chất lượng hình ảnh:** Độ phân giải, độ nét, màu sắc và độ tương phản của video có bất thường không?\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt có phù hợp với môi trường xung quanh không?\n* **Kết cấu da:** Da có trông thật tự nhiên hay có dấu hiệu bị làm mịn hoặc mờ?\n* **Hành vi bất thường:** Người trong video có hành động không phù hợp với ngữ cảnh hoặc có vẻ không tự nhiên?\n* **Âm thanh:** Giọng nói có phù hợp với hình ảnh và có vẻ tự nhiên không?\n\nHãy nhớ rằng, các deepfake ngày càng tinh vi, và việc xác định chúng có thể rất khó khăn. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[1],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Đây video này: ",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Đây là một deepfake khá tinh vi. Dù có những dấu hiệu nghi ngờ, nhưng việc khẳng định chắc chắn cần thêm phân tích và kỹ thuật chuyên môn.\n\n* **Chất lượng hình ảnh:** Video có độ phân giải cao, nhưng đôi lúc vẫn có thể thấy các lỗi nhỏ trong kết cấu da.\n* **Chuyển động:** Các chuyển động mắt và môi khá tự nhiên, nhưng có thể thấy một vài bất thường trong các chuyển động cơ mặt phức tạp.\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt tương đối phù hợp với môi trường xung quanh, tuy nhiên có thể có những điểm không đồng đều.\n\n**Để kết luận chính xác, cần phân tích kỹ hơn:**\n\n* Sử dụng các công cụ phân tích chuyên dụng để kiểm tra kỹ hơn về các lỗi nhỏ trong hình ảnh và chuyển động.\n* Phân tích tần suất khung hình và tìm kiếm các dấu hiệu bất thường trong chuyển động.\n* So sánh video với hình ảnh gốc của người thật để tìm kiếm sự khác biệt.\n\n**Kết luận:**\n\nDựa trên những phân tích sơ bộ, video này có khả năng là deepfake. Tuy nhiên, để xác định chắc chắn, cần thêm phân tích chuyên sâu.\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[2],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là của người thật hay deepfake",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Tôi cần thêm thông tin để xác định liệu video này là của người thật hay deepfake. \n\nHãy xem xét những điểm sau:\n\n* **Chất lượng hình ảnh:** Độ phân giải, độ nét, màu sắc và độ tương phản của video có bất thường không?\n* **Chuyển động:** Các chuyển động môi, mắt và cơ mặt có tự nhiên không?  Có dấu hiệu bất thường nào không?\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt có phù hợp với môi trường xung quanh không?\n* **Kết cấu da:** Da có trông thật tự nhiên hay có dấu hiệu bị làm mịn hoặc mờ?\n\nNgoài ra, hãy cho tôi biết bạn có cảm thấy bất kỳ điều gì bất thường trong video này không? \n\nCung cấp thêm chi tiết sẽ giúp tôi phân tích chính xác hơn.\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[3],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Đây, video này: ",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là một deepfake khá tinh vi, nhưng tôi có thể nhận thấy một số dấu hiệu bất thường:\n\n* **Kết cấu da:** Da của người phụ nữ trong video có vẻ hơi mờ và mịn, đặc biệt là ở vùng má và trán. Đây là một dấu hiệu của việc xử lý hậu kỳ để làm mịn da, điều mà thường được thấy trong deepfake.\n* **Chuyển động môi:** Chuyển động môi của người phụ nữ trong video không hoàn toàn khớp với lời thoại. Có thể thấy một sự chậm trễ nhỏ hoặc thiếu đồng bộ giữa lời thoại và cử động môi.\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt có vẻ không đồng đều, đặc biệt là ở vùng cổ. Điều này có thể do việc kết hợp hình ảnh từ các nguồn khác nhau trong quá trình tạo deepfake.\n\n**Tuy nhiên, để khẳng định chắc chắn, cần phân tích kỹ hơn:**\n\n* Sử dụng các công cụ phân tích chuyên dụng để kiểm tra kỹ hơn về các lỗi nhỏ trong hình ảnh và chuyển động.\n* Phân tích tần suất khung hình và tìm kiếm các dấu hiệu bất thường trong chuyển động.\n* So sánh video với hình ảnh gốc của người thật để tìm kiếm sự khác biệt.\n\n**Kết luận:**\n\nDựa trên những phân tích sơ bộ, video này có khả năng là deepfake. Tuy nhiên, để xác định chắc chắn, cần thêm phân tích chuyên sâu.\n\n \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[4],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này rất có khả năng là người thật. \n\nDù tôi không thể phân tích chi tiết mà không xem trực tiếp video, nhưng dựa trên các dấu hiệu thường gặp của deepfake, tôi thấy video này khá tự nhiên:\n\n* **Chất lượng hình ảnh:** Độ phân giải và độ nét của video không có gì bất thường.\n* **Chuyển động:** Các chuyển động mắt, môi, và cơ mặt đều khá tự nhiên, không có dấu hiệu bất thường về sự giật lag hay thiếu đồng bộ.\n* **Kết cấu da:** Da của người đàn ông trong video có vẻ tự nhiên, không có dấu hiệu bị làm mịn hoặc mờ bất thường.\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt phù hợp với môi trường xung quanh.\n\nTuy nhiên, để khẳng định chắc chắn, bạn có thể thử kiểm tra một số điểm sau:\n\n* **Âm thanh:** Nghe kỹ lời thoại và xem có bất kỳ dấu hiệu nào của sự bất thường về âm thanh, ví dụ như giọng nói nghe có vẻ nhân tạo hoặc có âm thanh méo mó.\n* **Cử động:** Quan sát kỹ cử động của cơ thể và đầu, xem có bất kỳ dấu hiệu nào của sự cứng nhắc hoặc thiếu tự nhiên.\n* **Bối cảnh:** Kiểm tra bối cảnh xung quanh để xem có bất kỳ điểm nào bất thường.\n\nHãy nhớ rằng, deepfake đang ngày càng tinh vi và việc xác định chúng có thể rất khó khăn. \n\n\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "Người thật bao nhiêu %",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Dựa trên phân tích sơ bộ, tôi đánh giá khả năng video này là người thật khoảng **90%**. \n\nTuy nhiên, tôi không thể khẳng định chắc chắn 100% mà không có thêm thông tin và phân tích chuyên sâu. \n\nCó thể có những chi tiết nhỏ mà tôi chưa nhận thấy, hoặc kỹ thuật deepfake đã tiến bộ đến mức khó có thể phân biệt được với mắt thường. \n\nĐể xác định chính xác, cần thêm phân tích chuyên sâu từ các chuyên gia sử dụng các công cụ và kỹ thuật chuyên dụng.\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[5],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là người thật hay deepfake",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này có khả năng cao là người thật. \n\nTuy nhiên, để khẳng định chắc chắn, tôi cần xem xét kỹ hơn các chi tiết sau:\n\n* **Chuyển động môi:** Chuyển động môi có tự nhiên và khớp với lời thoại không? \n* **Kết cấu da:** Da có trông thật tự nhiên hay có dấu hiệu bị làm mịn hoặc mờ?\n* **Cử động:** Cử động của người phụ nữ có tự nhiên và phù hợp với bối cảnh không?\n\nNếu bạn thấy bất kỳ dấu hiệu bất thường nào về chuyển động, kết cấu da hoặc cử động, thì video này có thể là deepfake.\n\nHãy nhớ rằng, deepfake ngày càng tinh vi và việc phát hiện chúng có thể rất khó khăn. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[6],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là người thật trên deepfake",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là deepfake. \n\nMặc dù nó được thực hiện rất tinh vi, nhưng có một số dấu hiệu cho thấy đây không phải là người thật:\n\n* **Kết cấu da:** Da của người phụ nữ trong video quá mịn màng và không có lỗ chân lông, một dấu hiệu thường thấy ở deepfake.\n* **Chuyển động mắt:**  Chuyển động mắt của người phụ nữ có vẻ không tự nhiên và hơi \"nhấp nháy\" khi cô ấy nhìn xung quanh. \n* **Chuyển động môi:**  Chuyển động môi không hoàn toàn khớp với lời thoại, có thể thấy một sự chậm trễ nhỏ.\n\nDeepfake ngày càng tinh vi, nhưng kỹ thuật của nó vẫn chưa hoàn hảo. \n\nHãy nhớ rằng, việc phát hiện deepfake đòi hỏi sự tập trung và phân tích kỹ lưỡng. \n\n \n\n\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[7],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[8],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là deepfake.\n\nMặc dù được thực hiện khá tinh vi, nhưng tôi có thể nhận thấy một số dấu hiệu bất thường:\n\n* **Kết cấu da:** Da của người phụ nữ trong video quá mịn màng và không có lỗ chân lông, một dấu hiệu thường thấy ở deepfake.\n* **Chuyển động mắt:** Chuyển động mắt của người phụ nữ có vẻ không tự nhiên và hơi \"nhấp nháy\" khi cô ấy nhìn xung quanh.\n* **Chuyển động môi:** Chuyển động môi không hoàn toàn khớp với lời thoại, có thể thấy một sự chậm trễ nhỏ.\n* **Bối cảnh:** Bối cảnh xung quanh có vẻ hơi kỳ lạ và không tự nhiên.\n\nDeepfake ngày càng tinh vi, nhưng kỹ thuật của nó vẫn chưa hoàn hảo.\n\nHãy nhớ rằng, việc phát hiện deepfake đòi hỏi sự tập trung và phân tích kỹ lưỡng. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          "Deepfake bao nhiêu %",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Dựa trên những dấu hiệu bất thường mà tôi đã phân tích, tôi đánh giá khả năng video này là deepfake khoảng 80%.\n\nTuy nhiên, việc xác định chắc chắn cần phân tích chuyên sâu hơn, bao gồm:\n\n* **Kiểm tra kỹ hơn về các lỗi nhỏ trong hình ảnh và chuyển động.**\n* **Phân tích tần suất khung hình để tìm kiếm các dấu hiệu bất thường.**\n* **So sánh video với hình ảnh gốc của người thật để tìm kiếm sự khác biệt.**\n\nDeepfake ngày càng tinh vi, việc đánh giá chính xác đòi hỏi chuyên môn và kỹ thuật chuyên dụng.\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[9],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là người thật. \n\nMặc dù công nghệ deepfake đang ngày càng tinh vi, nhưng tôi không thấy bất kỳ dấu hiệu nào cho thấy đây là deepfake trong video này. \n\n* **Kết cấu da:** Da của người phụ nữ có vẻ tự nhiên, với lỗ chân lông và nếp nhăn ở mức độ vừa phải. \n* **Chuyển động mắt:** Chuyển động mắt của cô ấy rất tự nhiên và không có dấu hiệu nào bất thường.\n* **Chuyển động môi:** Chuyển động môi khớp hoàn toàn với lời thoại.\n\nTôi không thể khẳng định chắc chắn mà không có thêm thông tin và phân tích chuyên sâu, nhưng dựa trên những gì tôi quan sát, video này rất có khả năng là người thật. \n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[10],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là một deepfake khá tinh vi. \n\nDù có những dấu hiệu nghi ngờ, nhưng việc khẳng định chắc chắn cần thêm phân tích và kỹ thuật chuyên môn.\n\n* **Chất lượng hình ảnh:** Video có độ phân giải cao, nhưng đôi lúc vẫn có thể thấy các lỗi nhỏ trong kết cấu da.\n* **Chuyển động:** Các chuyển động mắt và môi khá tự nhiên, nhưng có thể thấy một vài bất thường trong các chuyển động cơ mặt phức tạp.\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt tương đối phù hợp với môi trường xung quanh, tuy nhiên có thể có những điểm không đồng đều.\n\n**Để kết luận chính xác, cần phân tích kỹ hơn:**\n\n* Sử dụng các công cụ phân tích chuyên dụng để kiểm tra kỹ hơn về các lỗi nhỏ trong hình ảnh và chuyển động.\n* Phân tích tần suất khung hình và tìm kiếm các dấu hiệu bất thường trong chuyển động.\n* So sánh video với hình ảnh gốc của người thật để tìm kiếm sự khác biệt.\n\n**Kết luận:**\n\nDựa trên những phân tích sơ bộ, video này có khả năng là deepfake. Tuy nhiên, để xác định chắc chắn, cần thêm phân tích chuyên sâu.\n\n\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[11],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thường",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là người thật. \n\nDù tôi không thể phân tích chi tiết mà không xem trực tiếp video, nhưng dựa trên các dấu hiệu thường gặp của deepfake, tôi thấy video này khá tự nhiên:\n\n* **Chất lượng hình ảnh:** Độ phân giải và độ nét của video không có gì bất thường.\n* **Chuyển động:** Các chuyển động mắt, môi, và cơ mặt đều khá tự nhiên, không có dấu hiệu bất thường về sự giật lag hay thiếu đồng bộ.\n* **Kết cấu da:** Da của người đàn ông trong video có vẻ tự nhiên, không có dấu hiệu bị làm mịn hoặc mờ bất thường.\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt phù hợp với môi trường xung quanh.\n\nTuy nhiên, để khẳng định chắc chắn, bạn có thể thử kiểm tra một số điểm sau:\n\n* **Âm thanh:** Nghe kỹ lời thoại và xem có bất kỳ dấu hiệu nào của sự bất thường về âm thanh, ví dụ như giọng nói nghe có vẻ nhân tạo hoặc có âm thanh méo mó.\n* **Cử động:** Quan sát kỹ cử động của cơ thể và đầu, xem có bất kỳ dấu hiệu nào của sự cứng nhắc hoặc thiếu tự nhiên.\n* **Bối cảnh:** Kiểm tra bối cảnh xung quanh để xem có bất kỳ điểm nào bất thường.\n\nHãy nhớ rằng, deepfake đang ngày càng tinh vi và việc xác định chúng có thể rất khó khăn. \n\n\n\n\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[12],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thường",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là một deepfake. \n\nMặc dù được tạo ra khá tinh vi, nhưng tôi có thể nhận thấy một số dấu hiệu bất thường:\n\n* **Kết cấu da:** Da của người phụ nữ trong video quá mịn màng và không có lỗ chân lông, một dấu hiệu thường thấy ở deepfake.\n* **Chuyển động mắt:** Chuyển động mắt của người phụ nữ có vẻ không tự nhiên và hơi \"nhấp nháy\" khi cô ấy nhìn xung quanh. \n* **Chuyển động môi:** Chuyển động môi không hoàn toàn khớp với lời thoại, có thể thấy một sự chậm trễ nhỏ.\n\nDeepfake ngày càng tinh vi, nhưng kỹ thuật của nó vẫn chưa hoàn hảo.\n\nHãy nhớ rằng, việc phát hiện deepfake đòi hỏi sự tập trung và phân tích kỹ lưỡng. \n\n\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          files[13],
        ],
      },
      {
        "role": "user",
        "parts": [
          "Video này là deepfake hay người thật",
        ],
      },
      {
        "role": "model",
        "parts": [
          "Video này là deepfake. \n\nDù nó được thực hiện rất tinh vi, nhưng tôi có thể nhận thấy một số dấu hiệu bất thường:\n\n* **Kết cấu da:** Da của người đàn ông trong video có vẻ hơi mờ và mịn, đặc biệt là ở vùng cằm và cổ.\n* **Chuyển động:** Chuyển động của mắt, môi và cơ mặt có vẻ hơi cứng nhắc và không tự nhiên.\n* **Ánh sáng và bóng:** Ánh sáng và bóng trên khuôn mặt có vẻ không đồng đều, đặc biệt là ở vùng cằm và cổ.\n\nDeepfake ngày càng tinh vi, nhưng kỹ thuật của nó vẫn chưa hoàn hảo. \n\nHãy nhớ rằng, việc phát hiện deepfake đòi hỏi sự tập trung và phân tích kỹ lưỡng. \n\n \n\n\n\n\n",
        ],
      },
      {
        "role": "user",
        "parts": [
          video_up,
        ],
      },
    ]
  )

  response = chat_session.send_message("Đây là video deepfake hay người thật. Nếu là deepfake phản hồi 1, nếu là người thật phản hồi 0. Kèm theo % phía sau")

  print(response.text)

  return {"message": response.text}
