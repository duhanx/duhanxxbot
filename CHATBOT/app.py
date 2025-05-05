#AIzaSyACUuLBh7GOsBe4a3jQF70GkN-85hvgGo0
from flask import Flask , render_template , request
import os
import contextlib


# log kayıtlarını bastırma yani göstermeme

with open(os.devnull, 'w') as devnull , contextlib.redirect_stderr(devnull):
    import google.generativeai as genai
    
app = Flask(__name__)

#api anahtarını çağır

genai.configure(api_key = "AIzaSyACUuLBh7GOsBe4a3jQF70GkN-85hvgGo0")

generation_config = {
    "temperature" : 1,
    "top_p" : 0.95,
    "top_k" : 40,
    "max_output_tokens" : 8192,
    "response_mime_type" : "text/plain",

}

model = genai.GenerativeModel(
    model_name = "gemini-2.0-flash",
    generation_config=generation_config
)

corporate_text = (
    "Aşağıda \"Diyetim Takipte Sitesi\ için hazırlanmış bilgiler yer almaktadır."
    "Bu metin belgesinde websitemin iletişim bilgileri,çalışma saatlerimizi,diyetisyenlerimiz ve programlarımız hakkında temel bilgiler detaylandırılmıştır.\n\n"
    "----------------------------\n"
    "Diyetim Takipte Web Sitesi\n\n"
    "1.Web Sitesi Tanıtımı\n"   
    "Diyetim Takipte,diyetisyenler ve beslenme uzmanları için tasarlanmış bir yazılımdır."
    "Bu web sitesi ,diyetistenlerimizin yardımı, diyet planları ve ölçüm değerlendirme istatistikleri ile danışanların hedefine daha hızlı ve daha sağlıklı bir şekilde ulaşmasını hedeflemektedir.\n\n"
    "2.Çalışma Saatleri Ve Günleri\n\n"
    "Pazartesi-Cuma : 9AM - 6PM" \
    "Cumartesi: 9AM - 4PM" \
    "Pazar : Kapalı"
    "3.Abonelikler Ve Ücretlendirme\n\n"
    "Diyetim Takipte Sitesi bünyesinde aşağıdaki abonelikler sunulmaktadır."
    " 1 - Aylık : 450TL\n "
    " 3 - Aylık : 1000TL\n"
    " 12 - Aylık: 3000TL\n"
    "Cevap verirken bana bir danışanmışım gibi davran ve direkt sorduğum soruya tam cevap yada metinde bir yer görürsen oradaki veriyi aktar ve cevap verirken emoji kullan ki samimi gözükürsün."


)

#sohbet oturumunu oluştur
chat_session = model.start_chat(history=[])

#sohbeti başlat

conversation = [
    {"sender":"Diyetim Takipte","message":"Web Sitemize Hoşgeldiniz.Size Nasıl Yardımcı Olabilirim?"}
]

@app.route("/", methods=["GET", "POST"])
def chat():
    global conversation
    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        if user_input.lower() in ["exit", "quit"]:
            conversation.append({"sender": "Sistem", "message": "Sohbet sonlandırıldı."})
            return render_template("chat.html", conversation=conversation)
        
        # Kullanıcı mesajını sohbet geçmişine ekle
        conversation.append({"sender": "Danışan", "message": user_input})
        
        # Kullanıcının sorgusunu, kurumsal metinle birleştirerek modele gönderiyoruz
        combined_input = corporate_text + "\nSoru: " + user_input
        response = chat_session.send_message(combined_input)
        
        conversation.append({"sender": "ChatBot", "message": response.text})
    
    return render_template("chat.html", conversation=conversation)

if __name__ == "__main__":
    app.run(debug=True)