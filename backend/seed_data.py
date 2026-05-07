from database import engine, SessionLocal
from models import Base, Topic, Word

SEED_DATA = [
    {
        "name": "Chào hỏi",
        "description": "Các câu chào hỏi cơ bản",
        "icon": "👋",
        "words": [
            {"portuguese": "Olá", "vietnamese": "Xin chào", "example_pt": "Olá, como vai?", "example_vi": "Xin chào, bạn khỏe không?", "difficulty": 1},
            {"portuguese": "Bom dia", "vietnamese": "Chào buổi sáng", "example_pt": "Bom dia! Tudo bem?", "example_vi": "Chào buổi sáng! Mọi thứ ổn không?", "difficulty": 1},
            {"portuguese": "Boa tarde", "vietnamese": "Chào buổi chiều", "example_pt": "Boa tarde, senhor.", "example_vi": "Chào buổi chiều, thưa ông.", "difficulty": 1},
            {"portuguese": "Boa noite", "vietnamese": "Chào buổi tối / Chúc ngủ ngon", "example_pt": "Boa noite a todos.", "example_vi": "Chúc mọi người buổi tối vui vẻ.", "difficulty": 1},
            {"portuguese": "Como vai você?", "vietnamese": "Bạn có khỏe không?", "example_pt": "Como vai você hoje?", "example_vi": "Hôm nay bạn khỏe không?", "difficulty": 1},
            {"portuguese": "Tudo bem", "vietnamese": "Mọi thứ đều ổn", "example_pt": "Tudo bem, obrigado.", "example_vi": "Mọi thứ đều ổn, cảm ơn.", "difficulty": 1},
            {"portuguese": "Obrigado / Obrigada", "vietnamese": "Cảm ơn (nam/nữ)", "example_pt": "Muito obrigado pela ajuda.", "example_vi": "Cảm ơn rất nhiều vì đã giúp đỡ.", "difficulty": 1},
            {"portuguese": "De nada", "vietnamese": "Không có gì / Không sao", "example_pt": "— Obrigado! — De nada!", "example_vi": "— Cảm ơn! — Không có gì!", "difficulty": 1},
            {"portuguese": "Por favor", "vietnamese": "Làm ơn / Xin vui lòng", "example_pt": "Por favor, pode me ajudar?", "example_vi": "Làm ơn, bạn có thể giúp tôi không?", "difficulty": 1},
            {"portuguese": "Com licença", "vietnamese": "Xin lỗi (để qua)", "example_pt": "Com licença, posso passar?", "example_vi": "Xin lỗi, tôi có thể đi qua không?", "difficulty": 2},
            {"portuguese": "Desculpe", "vietnamese": "Xin lỗi (lỗi lầm)", "example_pt": "Desculpe pelo atraso.", "example_vi": "Xin lỗi vì đã đến trễ.", "difficulty": 2},
            {"portuguese": "Até logo", "vietnamese": "Tạm biệt (gặp lại sớm)", "example_pt": "Até logo, amigo!", "example_vi": "Tạm biệt, bạn ơi!", "difficulty": 1},
            {"portuguese": "Tchau", "vietnamese": "Tạm biệt (thân mật)", "example_pt": "Tchau, até amanhã!", "example_vi": "Tạm biệt, hẹn gặp ngày mai!", "difficulty": 1},
            {"portuguese": "Prazer", "vietnamese": "Hân hạnh được gặp", "example_pt": "Prazer em conhecer você.", "example_vi": "Hân hạnh được gặp bạn.", "difficulty": 2},
            {"portuguese": "Meu nome é...", "vietnamese": "Tên tôi là...", "example_pt": "Meu nome é Ana.", "example_vi": "Tên tôi là Ana.", "difficulty": 1},
            {"portuguese": "Eu sou...", "vietnamese": "Tôi là...", "example_pt": "Eu sou brasileiro.", "example_vi": "Tôi là người Brazil.", "difficulty": 1},
            {"portuguese": "Sim", "vietnamese": "Có / Vâng", "example_pt": "Sim, eu entendo.", "example_vi": "Vâng, tôi hiểu.", "difficulty": 1},
            {"portuguese": "Não", "vietnamese": "Không", "example_pt": "Não, obrigado.", "example_vi": "Không, cảm ơn.", "difficulty": 1},
            {"portuguese": "Fala português?", "vietnamese": "Bạn nói tiếng Bồ không?", "example_pt": "Você fala português?", "example_vi": "Bạn có nói tiếng Bồ Đào Nha không?", "difficulty": 2},
            {"portuguese": "Não entendo", "vietnamese": "Tôi không hiểu", "example_pt": "Desculpe, não entendo.", "example_vi": "Xin lỗi, tôi không hiểu.", "difficulty": 2},
        ]
    },
    {
        "name": "Số đếm",
        "description": "Số từ 0 đến 20",
        "icon": "🔢",
        "words": [
            {"portuguese": "zero", "vietnamese": "không (0)", "example_pt": "Zero graus.", "example_vi": "Không độ.", "difficulty": 1},
            {"portuguese": "um / uma", "vietnamese": "một (1)", "example_pt": "Um café, por favor.", "example_vi": "Một cà phê, làm ơn.", "difficulty": 1},
            {"portuguese": "dois / duas", "vietnamese": "hai (2)", "example_pt": "Dois irmãos.", "example_vi": "Hai anh em.", "difficulty": 1},
            {"portuguese": "três", "vietnamese": "ba (3)", "example_pt": "Três horas da tarde.", "example_vi": "Ba giờ chiều.", "difficulty": 1},
            {"portuguese": "quatro", "vietnamese": "bốn (4)", "example_pt": "Quatro estações do ano.", "example_vi": "Bốn mùa trong năm.", "difficulty": 1},
            {"portuguese": "cinco", "vietnamese": "năm (5)", "example_pt": "Cinco dedos.", "example_vi": "Năm ngón tay.", "difficulty": 1},
            {"portuguese": "seis", "vietnamese": "sáu (6)", "example_pt": "Seis dias.", "example_vi": "Sáu ngày.", "difficulty": 1},
            {"portuguese": "sete", "vietnamese": "bảy (7)", "example_pt": "Sete dias da semana.", "example_vi": "Bảy ngày trong tuần.", "difficulty": 1},
            {"portuguese": "oito", "vietnamese": "tám (8)", "example_pt": "Oito horas.", "example_vi": "Tám giờ.", "difficulty": 1},
            {"portuguese": "nove", "vietnamese": "chín (9)", "example_pt": "Nove meses.", "example_vi": "Chín tháng.", "difficulty": 1},
            {"portuguese": "dez", "vietnamese": "mười (10)", "example_pt": "Dez reais.", "example_vi": "Mười real.", "difficulty": 1},
            {"portuguese": "onze", "vietnamese": "mười một (11)", "example_pt": "Onze horas.", "example_vi": "Mười một giờ.", "difficulty": 2},
            {"portuguese": "doze", "vietnamese": "mười hai (12)", "example_pt": "Doze meses no ano.", "example_vi": "Mười hai tháng trong năm.", "difficulty": 2},
            {"portuguese": "treze", "vietnamese": "mười ba (13)", "example_pt": "Treze pessoas.", "example_vi": "Mười ba người.", "difficulty": 2},
            {"portuguese": "quatorze", "vietnamese": "mười bốn (14)", "example_pt": "Quatorze anos.", "example_vi": "Mười bốn tuổi.", "difficulty": 2},
            {"portuguese": "quinze", "vietnamese": "mười lăm (15)", "example_pt": "Quinze minutos.", "example_vi": "Mười lăm phút.", "difficulty": 2},
            {"portuguese": "dezesseis", "vietnamese": "mười sáu (16)", "example_pt": "Dezesseis graus.", "example_vi": "Mười sáu độ.", "difficulty": 2},
            {"portuguese": "dezessete", "vietnamese": "mười bảy (17)", "example_pt": "Dezessete reais.", "example_vi": "Mười bảy real.", "difficulty": 2},
            {"portuguese": "dezoito", "vietnamese": "mười tám (18)", "example_pt": "Dezoito anos.", "example_vi": "Mười tám tuổi.", "difficulty": 2},
            {"portuguese": "dezenove", "vietnamese": "mười chín (19)", "example_pt": "Dezenove horas.", "example_vi": "Mười chín giờ.", "difficulty": 2},
            {"portuguese": "vinte", "vietnamese": "hai mươi (20)", "example_pt": "Vinte pessoas.", "example_vi": "Hai mươi người.", "difficulty": 2},
        ]
    },
    {
        "name": "Màu sắc",
        "description": "Tên các màu sắc cơ bản",
        "icon": "🎨",
        "words": [
            {"portuguese": "vermelho", "vietnamese": "màu đỏ", "example_pt": "O carro é vermelho.", "example_vi": "Chiếc xe màu đỏ.", "difficulty": 1},
            {"portuguese": "azul", "vietnamese": "màu xanh dương", "example_pt": "O céu é azul.", "example_vi": "Bầu trời màu xanh dương.", "difficulty": 1},
            {"portuguese": "verde", "vietnamese": "màu xanh lá", "example_pt": "A árvore é verde.", "example_vi": "Cái cây màu xanh lá.", "difficulty": 1},
            {"portuguese": "amarelo", "vietnamese": "màu vàng", "example_pt": "O sol é amarelo.", "example_vi": "Mặt trời màu vàng.", "difficulty": 1},
            {"portuguese": "preto", "vietnamese": "màu đen", "example_pt": "O gato é preto.", "example_vi": "Con mèo màu đen.", "difficulty": 1},
            {"portuguese": "branco", "vietnamese": "màu trắng", "example_pt": "A neve é branca.", "example_vi": "Tuyết màu trắng.", "difficulty": 1},
            {"portuguese": "laranja", "vietnamese": "màu cam", "example_pt": "A laranja é laranja.", "example_vi": "Quả cam màu cam.", "difficulty": 1},
            {"portuguese": "rosa", "vietnamese": "màu hồng", "example_pt": "As flores são rosas.", "example_vi": "Những bông hoa màu hồng.", "difficulty": 1},
            {"portuguese": "roxo", "vietnamese": "màu tím", "example_pt": "O vestido é roxo.", "example_vi": "Chiếc váy màu tím.", "difficulty": 2},
            {"portuguese": "marrom", "vietnamese": "màu nâu", "example_pt": "O chocolate é marrom.", "example_vi": "Sô-cô-la màu nâu.", "difficulty": 2},
            {"portuguese": "cinza", "vietnamese": "màu xám", "example_pt": "As nuvens são cinzas.", "example_vi": "Những đám mây màu xám.", "difficulty": 2},
            {"portuguese": "dourado", "vietnamese": "màu vàng kim", "example_pt": "O anel é dourado.", "example_vi": "Chiếc nhẫn màu vàng kim.", "difficulty": 2},
        ]
    },
    {
        "name": "Đồ ăn & Đồ uống",
        "description": "Tên các món ăn và đồ uống",
        "icon": "🍽️",
        "words": [
            {"portuguese": "água", "vietnamese": "nước", "example_pt": "Eu quero água, por favor.", "example_vi": "Tôi muốn nước, làm ơn.", "difficulty": 1},
            {"portuguese": "café", "vietnamese": "cà phê", "example_pt": "Um café com leite.", "example_vi": "Một cà phê sữa.", "difficulty": 1},
            {"portuguese": "leite", "vietnamese": "sữa", "example_pt": "Eu tomo leite pela manhã.", "example_vi": "Tôi uống sữa vào buổi sáng.", "difficulty": 1},
            {"portuguese": "suco", "vietnamese": "nước ép", "example_pt": "Suco de laranja, por favor.", "example_vi": "Nước ép cam, làm ơn.", "difficulty": 1},
            {"portuguese": "pão", "vietnamese": "bánh mì", "example_pt": "Eu como pão no café da manhã.", "example_vi": "Tôi ăn bánh mì vào bữa sáng.", "difficulty": 1},
            {"portuguese": "arroz", "vietnamese": "cơm / gạo", "example_pt": "Arroz com feijão.", "example_vi": "Cơm với đậu đen.", "difficulty": 1},
            {"portuguese": "feijão", "vietnamese": "đậu đen", "example_pt": "Feijão preto é delicioso.", "example_vi": "Đậu đen rất ngon.", "difficulty": 2},
            {"portuguese": "frango", "vietnamese": "thịt gà", "example_pt": "Frango grelhado.", "example_vi": "Gà nướng.", "difficulty": 2},
            {"portuguese": "carne", "vietnamese": "thịt", "example_pt": "Carne de boi.", "example_vi": "Thịt bò.", "difficulty": 2},
            {"portuguese": "peixe", "vietnamese": "cá", "example_pt": "Peixe frito.", "example_vi": "Cá chiên.", "difficulty": 1},
            {"portuguese": "salada", "vietnamese": "rau trộn / salad", "example_pt": "Uma salada verde.", "example_vi": "Một đĩa rau trộn.", "difficulty": 2},
            {"portuguese": "fruta", "vietnamese": "trái cây", "example_pt": "Eu gosto de fruta.", "example_vi": "Tôi thích trái cây.", "difficulty": 1},
            {"portuguese": "maçã", "vietnamese": "táo", "example_pt": "Uma maçã por dia.", "example_vi": "Một quả táo mỗi ngày.", "difficulty": 2},
            {"portuguese": "banana", "vietnamese": "chuối", "example_pt": "Banana com aveia.", "example_vi": "Chuối với yến mạch.", "difficulty": 1},
            {"portuguese": "sobremesa", "vietnamese": "tráng miệng", "example_pt": "O que tem de sobremesa?", "example_vi": "Có gì để tráng miệng?", "difficulty": 3},
            {"portuguese": "bolo", "vietnamese": "bánh ngọt / bánh kem", "example_pt": "Bolo de chocolate.", "example_vi": "Bánh kem sô-cô-la.", "difficulty": 2},
            {"portuguese": "delicioso", "vietnamese": "ngon / thơm ngon", "example_pt": "Isso está delicioso!", "example_vi": "Cái này thật ngon!", "difficulty": 2},
        ]
    },
    {
        "name": "Gia đình",
        "description": "Các từ về thành viên gia đình",
        "icon": "👨‍👩‍👧‍👦",
        "words": [
            {"portuguese": "família", "vietnamese": "gia đình", "example_pt": "Minha família é grande.", "example_vi": "Gia đình tôi đông người.", "difficulty": 1},
            {"portuguese": "pai", "vietnamese": "bố / ba", "example_pt": "Meu pai trabalha muito.", "example_vi": "Bố tôi làm việc rất chăm chỉ.", "difficulty": 1},
            {"portuguese": "mãe", "vietnamese": "mẹ", "example_pt": "Minha mãe cozinha bem.", "example_vi": "Mẹ tôi nấu ăn rất ngon.", "difficulty": 1},
            {"portuguese": "filho", "vietnamese": "con trai", "example_pt": "Tenho um filho.", "example_vi": "Tôi có một con trai.", "difficulty": 1},
            {"portuguese": "filha", "vietnamese": "con gái", "example_pt": "Minha filha tem cinco anos.", "example_vi": "Con gái tôi năm tuổi.", "difficulty": 1},
            {"portuguese": "irmão", "vietnamese": "anh / em trai", "example_pt": "Meu irmão mais velho.", "example_vi": "Anh trai của tôi.", "difficulty": 1},
            {"portuguese": "irmã", "vietnamese": "chị / em gái", "example_pt": "Tenho duas irmãs.", "example_vi": "Tôi có hai chị em gái.", "difficulty": 1},
            {"portuguese": "avô", "vietnamese": "ông nội / ngoại", "example_pt": "Meu avô tem 70 anos.", "example_vi": "Ông tôi 70 tuổi.", "difficulty": 2},
            {"portuguese": "avó", "vietnamese": "bà nội / ngoại", "example_pt": "Minha avó faz bolo.", "example_vi": "Bà tôi làm bánh.", "difficulty": 2},
            {"portuguese": "tio", "vietnamese": "chú / cậu / bác (nam)", "example_pt": "Meu tio mora em Lisboa.", "example_vi": "Chú tôi sống ở Lisbon.", "difficulty": 2},
            {"portuguese": "tia", "vietnamese": "cô / dì / bác (nữ)", "example_pt": "Minha tia é professora.", "example_vi": "Cô tôi là giáo viên.", "difficulty": 2},
            {"portuguese": "primo / prima", "vietnamese": "anh/chị/em họ", "example_pt": "Meu primo é médico.", "example_vi": "Anh họ tôi là bác sĩ.", "difficulty": 2},
            {"portuguese": "marido", "vietnamese": "chồng", "example_pt": "Meu marido é simpático.", "example_vi": "Chồng tôi rất tốt bụng.", "difficulty": 2},
            {"portuguese": "esposa", "vietnamese": "vợ", "example_pt": "Minha esposa gosta de música.", "example_vi": "Vợ tôi thích âm nhạc.", "difficulty": 2},
            {"portuguese": "bebê", "vietnamese": "em bé / trẻ sơ sinh", "example_pt": "O bebê está dormindo.", "example_vi": "Em bé đang ngủ.", "difficulty": 1},
        ]
    },
    {
        "name": "Thời gian",
        "description": "Ngày trong tuần và tháng trong năm",
        "icon": "📅",
        "words": [
            {"portuguese": "hoje", "vietnamese": "hôm nay", "example_pt": "O que você faz hoje?", "example_vi": "Hôm nay bạn làm gì?", "difficulty": 1},
            {"portuguese": "amanhã", "vietnamese": "ngày mai", "example_pt": "Até amanhã!", "example_vi": "Hẹn gặp ngày mai!", "difficulty": 1},
            {"portuguese": "ontem", "vietnamese": "hôm qua", "example_pt": "Ontem foi ótimo.", "example_vi": "Hôm qua thật tuyệt.", "difficulty": 1},
            {"portuguese": "segunda-feira", "vietnamese": "Thứ Hai", "example_pt": "Na segunda-feira tenho aula.", "example_vi": "Thứ Hai tôi có lớp học.", "difficulty": 2},
            {"portuguese": "terça-feira", "vietnamese": "Thứ Ba", "example_pt": "Terça-feira é dia de reunião.", "example_vi": "Thứ Ba là ngày họp.", "difficulty": 2},
            {"portuguese": "quarta-feira", "vietnamese": "Thứ Tư", "example_pt": "Na quarta vou ao mercado.", "example_vi": "Thứ Tư tôi đi chợ.", "difficulty": 2},
            {"portuguese": "quinta-feira", "vietnamese": "Thứ Năm", "example_pt": "Quinta é meu dia favorito.", "example_vi": "Thứ Năm là ngày yêu thích của tôi.", "difficulty": 2},
            {"portuguese": "sexta-feira", "vietnamese": "Thứ Sáu", "example_pt": "Sexta é dia de festa!", "example_vi": "Thứ Sáu là ngày vui chơi!", "difficulty": 2},
            {"portuguese": "sábado", "vietnamese": "Thứ Bảy", "example_pt": "Sábado eu descanso.", "example_vi": "Thứ Bảy tôi nghỉ ngơi.", "difficulty": 1},
            {"portuguese": "domingo", "vietnamese": "Chủ Nhật", "example_pt": "Domingo é dia de família.", "example_vi": "Chủ Nhật là ngày gia đình.", "difficulty": 1},
            {"portuguese": "semana", "vietnamese": "tuần", "example_pt": "Esta semana está ocupada.", "example_vi": "Tuần này rất bận.", "difficulty": 1},
            {"portuguese": "mês", "vietnamese": "tháng", "example_pt": "Este mês é especial.", "example_vi": "Tháng này rất đặc biệt.", "difficulty": 1},
            {"portuguese": "ano", "vietnamese": "năm", "example_pt": "Feliz Ano Novo!", "example_vi": "Chúc mừng Năm Mới!", "difficulty": 1},
            {"portuguese": "hora", "vietnamese": "giờ", "example_pt": "Que horas são?", "example_vi": "Mấy giờ rồi?", "difficulty": 1},
            {"portuguese": "minuto", "vietnamese": "phút", "example_pt": "Espera um minuto.", "example_vi": "Đợi một phút.", "difficulty": 1},
            {"portuguese": "manhã", "vietnamese": "buổi sáng", "example_pt": "Bom dia de manhã!", "example_vi": "Chào buổi sáng!", "difficulty": 1},
            {"portuguese": "tarde", "vietnamese": "buổi chiều", "example_pt": "À tarde vou passear.", "example_vi": "Buổi chiều tôi đi dạo.", "difficulty": 1},
            {"portuguese": "noite", "vietnamese": "buổi tối", "example_pt": "À noite eu leio.", "example_vi": "Buổi tối tôi đọc sách.", "difficulty": 1},
        ]
    }
]

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Topic).count() > 0:
            print("Database already seeded.")
            return
        for topic_data in SEED_DATA:
            topic = Topic(
                name=topic_data["name"],
                description=topic_data["description"],
                icon=topic_data["icon"]
            )
            db.add(topic)
            db.flush()
            for word_data in topic_data["words"]:
                word = Word(topic_id=topic.id, **word_data)
                db.add(word)
        db.commit()
        print(f"Seeded {len(SEED_DATA)} topics successfully.")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed()
