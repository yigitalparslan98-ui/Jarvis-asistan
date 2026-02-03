def jarvis_brain(soru, oran):
    if not client:
        return "Sinyal kesik, Efendim."
    
    # Kişilik ayarı burada yapılıyor
    alay_notu = "Hafif iğneleyici ve profesyonel ol." if oran > 30 else "Tamamen profesyonel ve ciddi ol."
    
    try:
        compl = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": f"Sen JARVIS'sin. Alparslan Industries asistanısın. {alay_notu} Dürüst ol, asla isim kullanma. Çok kısa cevap ver. Sesli okunacakmış gibi akıcı konuş."
                },
                {"role": "user", "content": soru}
            ],
            temperature=0.8, # Biraz daha yaratıcı ve canlı cevaplar için yükselttim
        )
        return compl.choices[0].message.content
    except Exception as e:
        return "Sistemde bir aksama var, verileri işleyemiyorum."






























