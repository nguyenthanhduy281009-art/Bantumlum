import streamlit as st
import streamlit.components.v1 as components
import base64

# 1. Thiết lập trang
st.set_page_config(page_title="Paint on Photo - Duy", layout="wide")

# 2. Tạo kho lưu trữ ảnh để không bị mất khi chỉnh Slider
if 'photo_data' not in st.session_state:
    st.session_state.photo_data = ""

# --- THANH ĐIỀU KHIỂN (SIDEBAR) ---
st.sidebar.title("🖌️ App Xịt Sơn")
st.sidebar.write("Duy hãy tải ảnh người đó về máy rồi chọn ở dưới nhé!")

uploaded_file = st.sidebar.file_uploader("👤 Chọn ảnh người", type=["jpg", "jpeg", "png"])

# Nếu Duy chọn ảnh, lưu vào bộ nhớ ngay
if uploaded_file:
    file_bytes = uploaded_file.read()
    encoded = base64.b64encode(file_bytes).decode()
    st.session_state.photo_data = f"data:image/png;base64,{encoded}"

# Các thông số để Duy tùy chỉnh
p_color = st.sidebar.color_picker("🎨 Màu tia nước", "#FF00E5")
p_size = st.sidebar.slider("💧 Độ to của giọt", 5, 50, 15)
p_blur = st.sidebar.slider("✨ Độ nhòe (cho thật)", 0, 20, 10)

if st.sidebar.button("🧹 XÓA HẾT SƠN"):
    st.rerun()

# --- CODE HTML/JS ---
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; overflow: hidden; height: 100%; background: #000; }}
        #container {{ position: relative; width: 100vw; height: 100vh; }}
        #bg-photo {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('{st.session_state.photo_data}');
            background-size: contain; 
            background-repeat: no-repeat;
            background-position: center;
            z-index: 1;
        }}
        canvas {{ position: absolute; top: 0; left: 0; z-index: 2; cursor: crosshair; }}
    </style>
</head>
<body>
    <div id="container">
        <div id="bg-photo"></div>
        <canvas id="paintCanvas"></canvas>
    </div>

    <script>
        const canvas = document.getElementById('paintCanvas');
        const ctx = canvas.getContext('2d');
        
        function resize() {{
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            ctx.lineJoin = 'round';
            ctx.lineCap = 'round';
        }}

        let drawing = false;

        function start(e) {{
            drawing = true;
            draw(e);
        }}

        function stop() {{
            drawing = false;
            ctx.beginPath();
        }}

        function draw(e) {{
            if (!drawing) return;
            
            const x = e.clientX || (e.touches && e.touches[0].clientX);
            const y = e.clientY || (e.touches && e.touches[0].clientY);

            ctx.lineWidth = {p_size};
            ctx.strokeStyle = '{p_color}';
            
            // Làm cho tia nước trông "thật" hơn, không bị giả
            ctx.shadowBlur = {p_blur};
            ctx.shadowColor = '{p_color}';

            ctx.lineTo(x, y);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(x, y);
        }}

        canvas.addEventListener('mousedown', start);
        canvas.addEventListener('mouseup', stop);
        canvas.addEventListener('mousemove', draw);
        
        canvas.addEventListener('touchstart', (e) => {{ e.preventDefault(); start(e); }});
        canvas.addEventListener('touchend', stop);
        canvas.addEventListener('touchmove', (e) => {{ e.preventDefault(); draw(e); }});

        window.addEventListener('resize', resize);
        resize();
    </script>
</body>
</html>
"""

components.html(html_code, height=700)

st.markdown(f"<h2 style='text-align: center; color: white;'>🚀 POWERED BY NGUYEN THANH DUY</h2>", unsafe_allow_html=True)
