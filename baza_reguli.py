REGULI_MATEMATICE = [

    {
        "id": "teorema_tetratie",
        "descriere": r"Turn infinit de puteri, exponențieri repetate la infinit, x la puterea x la infinit.",
        "hint": r"ATENȚIE: Un turn infinit de puteri converge doar pentru o valoare <= e^(1/e) ≈ 1.4447. Dacă valoarea este mai mare, ecuația nu are soluție reală. Răspunde cu \boxed{fara_solutie}."
    },
    {
        "id": "capcana_numitorului",
        "descriere": r"Ecuații raționale, fracții cu x la numitor, împărțiri la o expresie cu x.",
        "hint": r"ATENȚIE: Nu uita de domeniul de definiție! Verifică dacă soluția obținută nu anulează numitorul (împărțirea la zero). Elimină soluțiile false înainte de a scrie rezultatul."
    },
    {
        "id": "conditie_logaritmi",
        "descriere": r"Ecuații logaritmice, logaritmi, log, ln(x), lg(x), sumă sau diferență de logaritmi.",
        "hint": r"ATENȚIE: Pentru orice ecuație logaritmică, argumentul logaritmului trebuie să fie STRICT POZITIV (> 0). Baza logaritmului trebuie să fie > 0 și diferită de 1. Verifică soluțiile și elimină-le pe cele false!"
    },
    {
        "id": "radicali_ordin_par",
        "descriere": r"Radicali de ordin par, rădăcină pătrată, sqrt(x), ecuații iraționale cu radical din x.",
        "hint": r"ATENȚIE: Cantitatea de sub un radical de ordin par trebuie să fie >= 0. Rezultatul unui radical de ordin par este mereu >= 0. Ridicarea la pătrat poate introduce soluții false (străine). Verifică soluțiile la final!"
    },
    {
        "id": "valoare_absoluta_modul",
        "descriere": r"Modul din x, valoare absolută, |x|, ecuații cu modul.",
        "hint": r"ATENȚIE: Modulul oricărui număr real este mereu >= 0. O ecuație de forma |E(x)| = a, unde a < 0, nu are soluții reale. Tratează cazurile E(x) >= 0 și E(x) < 0 separat!"
    },
    {
        "id": "inecuatii_logaritmice_baza_subunitara",
        "descriere": r"Inecuații logaritmice sau exponențiale unde baza este un număr între 0 și 1.",
        "hint": r"ATENȚIE: Dacă baza este subunitară (0 < b < 1), la renunțarea la logaritm/exponențială, SENSUL INEGALITĂȚII SE SCHIMBĂ (< devine >, etc.)."
    },
    {
        "id": "impartire_la_expresie_cu_x",
        "descriere": r"Împărțirea ambilor membri ai unei ecuații sau inecuații la o expresie care conține x.",
        "hint": r"ATENȚIE: Când împarți o inecuație la o expresie cu x, semnul inegalității SE SCHIMBĂ dacă expresia respectivă este negativă. Analizează semnul expresiei înainte de a împărți, tratând cazurile pozitiv și negativ separat!"
    },
    {
        "id": "ecuatia_patratica_discriminant",
        "descriere": r"Ecuație de gradul 2, ax^2 + bx + c = 0, discriminant delta.",
        "hint": r"ATENȚIE: Soluțiile reale există DOAR dacă discriminantul Δ = b² - 4ac >= 0. Dacă Δ < 0, ecuația nu are soluții reale. Dacă Δ = 0, există o singură soluție (rădăcină dublă) x = -b/(2a)."
    },
    {
        "id": "ridicare_la_putere_para_inecuatie",
        "descriere": r"Ridicarea la o putere pară (2, 4, ...) a ambilor membri ai unei inecuații.",
        "hint": r"ATENȚIE: Ridicarea la o putere pară presupune că AMBII membri sunt nenegativi. Dacă un membru poate fi negativ, trebuie să tratezi cazurile separat. Acest pas poate introduce inegalități false!"
    },
    {
        "id": "impartire_prin_zero",
        "descriere": r"Simplificarea unei expresii prin împărțire, reducerea unui factor comun.",
        "hint": r"ATENȚIE: Nu simplifica prin împărțire la o expresie care ar putea fi zero! Dacă simplifici x din x·f(x) = x·g(x), poți pierde soluția x = 0. Factorizează și analizează fiecare caz separat."
    },
    {
        "id": "ecuatia_modulului_patratic",
        "descriere": r"Ecuație cu modul de forma |ax^2 + bx + c| = d sau |f(x)| = |g(x)|.",
        "hint": r"ATENȚIE: Ecuația |f(x)| = |g(x)| este echivalentă cu f(x) = g(x) SAU f(x) = -g(x). Rezolvă ambele cazuri și verifică soluțiile în ecuația originală."
    },
    {
        "id": "sistem_cramer_determinant_zero",
        "descriere": r"Sistem de ecuații liniare, metodă Cramer, determinant, matrice.",
        "hint": r"ATENȚIE: Metoda Cramer funcționează DOAR dacă determinantul matricei sistemului este nenul (det ≠ 0). Dacă det = 0, sistemul poate fi incompatibil (fără soluții) sau compatibil nedeterminat (infinit de soluții). Verifică rangul!"
    },
    {
        "id": "numere_complexe_modul",
        "descriere": r"Numere complexe, modul complex, |z|, argument, formă trigonometrică.",
        "hint": r"ATENȚIE: Modulul unui număr complex z = a + bi este |z| = sqrt(a² + b²), care este mereu >= 0. Forma trigonometrică necesită calculul corect al argumentului (unghiului) ținând cont de cadranul în care se află z."
    },
    {
        "id": "putere_numar_complex",
        "descriere": r"Ridicarea unui număr complex la putere, formula lui De Moivre, z^n.",
        "hint": r"ATENȚIE: Pentru calculul z^n, convertește la forma trigonometrică z = r(cosθ + i·sinθ), apoi aplică formula De Moivre: z^n = r^n(cos(nθ) + i·sin(nθ)). Nu ridica direct partea reală și imaginară la putere!"
    },
    {
        "id": "radacina_din_numar_complex",
        "descriere": r"Rădăcini ale unui număr complex, rădăcini de ordinul n din z.",
        "hint": r"ATENȚIE: Ecuația z^n = w are EXACT n soluții complexe distincte. Soluțiile sunt w_k = r^(1/n) · (cos((θ + 2kπ)/n) + i·sin((θ + 2kπ)/n)) pentru k = 0, 1, ..., n-1. Nu uita niciuna din cele n rădăcini!"
    },
    {
        "id": "relatiile_lui_vieta",
        "descriere": r"Suma și produsul rădăcinilor unui polinom, relațiile Viète, x1+x2, x1·x2.",
        "hint": r"ATENȚIE: Relațiile lui Viète se aplică NUMAI dacă ecuația are soluții reale (Δ >= 0). Suma rădăcinilor x1+x2 = -b/a și produsul x1·x2 = c/a. Nu le confunda! Verifică întotdeauna că discriminantul este nenegativ."
    },
    {
        "id": "ecuatie_biquadratica",
        "descriere": r"Ecuație biquadratică, ax^4 + bx^2 + c = 0, substituție t = x^2.",
        "hint": r"ATENȚIE: La substituția t = x^2, soluțiile t obținute trebuie să fie >= 0 pentru a putea extrage rădăcina pătrată. Dacă t < 0, acea soluție nu generează soluții reale pentru x. Fiecare t > 0 generează DOUĂ soluții pentru x: x = ±√t."
    },
    {
        "id": "inegalitatea_am_gm",
        "descriere": r"Inegalitatea mediei aritmetice și geometrice, AM-GM, a+b >= 2sqrt(ab).",
        "hint": r"ATENȚIE: Inegalitatea AM-GM (media aritmetică >= media geometrică) se aplică NUMAI pentru numere nenegative (>= 0). Egalitatea are loc DOAR când toate numerele sunt egale între ele. Nu aplica AM-GM pe numere negative!"
    },
    {
        "id": "sir_telescopic",
        "descriere": r"Sumă telescopică, serii telescopice, sumă de diferențe consecutive f(n+1) - f(n).",
        "hint": r"ATENȚIE: Suma telescopică de forma Σ[f(k+1) - f(k)] de la k=1 la n se simplifică la f(n+1) - f(1). Identifică structura telescopică și scrie primii și ultimii termeni pentru a vedea ce se anulează."
    },
    {
        "id": "numere_prime_si_compuse",
        "descriere": r"Numere prime, descompunere în factori primi, CMMDC, CMMMC.",
        "hint": r"ATENȚIE: 1 nu este număr prim. Numărul 2 este singurul număr prim par. CMMDC(a,b) × CMMMC(a,b) = a × b. Dacă CMMDC(a,b) = 1, numerele sunt coprime (prime între ele)."
    },

    # ================================================================
    # SECȚIUNEA 2: TRIGONOMETRIE
    # ================================================================

    {
        "id": "domeniu_arcsin_arccos",
        "descriere": r"Funcții trigonometrice inverse, arcsin(x), arccos(x).",
        "hint": r"ATENȚIE: Domeniul de definiție pentru arcsin(x) și arccos(x) este [-1, 1]. Dacă argumentul depășește aceste limite, ecuația nu are soluții reale."
    },
    {
        "id": "impartire_trigonometrica_zero",
        "descriere": r"Ecuații trigonometrice cu tangenta, cotangenta, împărțire prin sin(x) sau cos(x).",
        "hint": r"ATENȚIE: Când împarți o ecuație prin sin(x) sau cos(x), verifică separat și cazurile sin(x) = 0 sau cos(x) = 0. Poți pierde soluții importante!"
    },
    {
        "id": "solutii_periodice_trigonometrie",
        "descriere": r"Ecuații trigonometrice, soluții generale, sin(x) = a, cos(x) = a, perioada.",
        "hint": r"ATENȚIE: Ecuațiile trigonometrice au în general infinit de soluții datorită periodicității. Soluția generală pentru sin(x) = a este x = arcsin(a) + 2kπ SAU x = π - arcsin(a) + 2kπ, k ∈ ℤ. Pentru cos(x) = a: x = ±arccos(a) + 2kπ. Nu uita de perioada funcției!"
    },
    {
        "id": "identitate_pitagoreica",
        "descriere": r"Identitate fundamentală trigonometrică, sin^2(x) + cos^2(x) = 1.",
        "hint": r"ATENȚIE: Identitatea fundamentală sin²(x) + cos²(x) = 1 este mereu adevărată. Din ea derivă: 1 + tan²(x) = 1/cos²(x) și 1 + cot²(x) = 1/sin²(x). Folosește-o pentru a reduce expresii cu sin și cos."
    },
    {
        "id": "formule_adunare_trigonometrie",
        "descriere": r"Formule de adunare, sin(a+b), cos(a+b), sin(a-b), cos(a-b), tan(a+b).",
        "hint": r"ATENȚIE: sin(a+b) = sin(a)cos(b) + cos(a)sin(b) și cos(a+b) = cos(a)cos(b) - sin(a)sin(b). Nu confunda semnele! La cos(a+b) semnul este minus, pe când la sin(a+b) este plus."
    },
    {
        "id": "formule_dublului_unghi",
        "descriere": r"Formule pentru unghiul dublu, sin(2x), cos(2x), tan(2x).",
        "hint": r"ATENȚIE: sin(2x) = 2·sin(x)·cos(x). cos(2x) are TREI forme echivalente: cos²x - sin²x = 2cos²x - 1 = 1 - 2sin²x. Alege forma potrivită contextului pentru simplificări mai ușoare."
    },
    {
        "id": "transformare_suma_in_produs",
        "descriere": r"Transformarea sumei sau diferenței de sinus/cosinus în produs (prosthaphaeresis).",
        "hint": r"ATENȚIE: sin(a) + sin(b) = 2·sin((a+b)/2)·cos((a-b)/2). sin(a) - sin(b) = 2·cos((a+b)/2)·sin((a-b)/2). Aceste formule sunt utile când vrei să factorizezi sau să anulezi expresii trigonometrice."
    },
    {
        "id": "domeniu_tangenta_cotangenta",
        "descriere": r"Tangenta, cotangenta, tg(x), ctg(x), domeniu de definiție.",
        "hint": r"ATENȚIE: tan(x) nu este definită pentru x = π/2 + kπ (unde cos(x) = 0). cot(x) nu este definită pentru x = kπ (unde sin(x) = 0). Exclude aceste valori din domeniu!"
    },
    {
        "id": "inegalitati_trigonometrice",
        "descriere": r"Inecuații trigonometrice, sin(x) > a, cos(x) < b, rezolvare pe cerc trigonometric.",
        "hint": r"ATENȚIE: La rezolvarea inecuațiilor trigonometrice, reprezintă soluțiile pe cercul trigonometric. Atenție la direcția parcurgerii (sens trigonometric = anti-orar). Soluția este un arc de cerc, nu un punct!"
    },
    {
        "id": "formula_lui_euler",
        "descriere": r"Formula lui Euler, e^(ix) = cos(x) + i·sin(x), legătura cu numerele complexe.",
        "hint": r"ATENȚIE: Formula lui Euler e^(ix) = cos(x) + i·sin(x) leagă funcțiile trigonometrice de exponențiale complexe. Din ea: cos(x) = (e^(ix) + e^(-ix))/2 și sin(x) = (e^(ix) - e^(-ix))/(2i). Caz special celebru: e^(iπ) + 1 = 0."
    },

    # ================================================================
    # SECȚIUNEA 3: ANALIZĂ MATEMATICĂ – LIMITE ȘI CONTINUITATE
    # ================================================================

    {
        "id": "limite_forme_nedeterminate",
        "descriere": r"Limite de funcții, forme nedeterminate, 0/0, infinit/infinit, regula lui l'Hopital.",
        "hint": r"ATENȚIE: Aplică Regula lui l'Hôpital NUMAI dacă limita este de forma 0/0 sau ∞/∞. Aplică-o pe numărător și numitor SEPARAT (nu folosind regula câtului!). Dacă după aplicare apare din nou o formă nedeterminată, poți reaplica regula."
    },
    {
        "id": "continuitate_functie",
        "descriere": r"Continuitatea unei funcții, funcție continuă, limita laterală, salt de discontinuitate.",
        "hint": r"ATENȚIE: O funcție este continuă în x₀ DACĂ ȘI NUMAI DACĂ: (1) f(x₀) este definit, (2) limita există (limitele laterale sunt egale), (3) limita este egală cu valoarea funcției. Verifică toate trei condiții!"
    },
    {
        "id": "limita_remarcabila_sinx_x",
        "descriere": r"Limita remarcabilă sin(x)/x, lim sin(x)/x când x->0.",
        "hint": r"ATENȚIE: Limita remarcabilă lim(x→0) sin(x)/x = 1 este adevărată NUMAI când x este în radiani. Dacă x este în grade, formula se modifică. De asemenea, lim(x→0) (1-cos(x))/x² = 1/2."
    },
    {
        "id": "limita_remarcabila_e",
        "descriere": r"Numărul lui Euler e, limita (1 + 1/n)^n, (1 + x)^(1/x).",
        "hint": r"ATENȚIE: lim(n→∞) (1 + 1/n)^n = e ≈ 2.718. Mai general: lim(x→0) (1 + x)^(1/x) = e. Forma (1 + α(x))^(1/α(x)) → e dacă α(x) → 0. Identifică structura pentru a aplica corect."
    },
    {
        "id": "teorema_sandwich_squeeze",
        "descriere": r"Teorema cleștelui (sandwich), inegalități pentru limite, g(x) <= f(x) <= h(x).",
        "hint": r"ATENȚIE: Dacă g(x) ≤ f(x) ≤ h(x) în jurul lui x₀ și lim g(x) = lim h(x) = L, atunci lim f(x) = L. Utilă pentru limite de forma sin(x)·funcție_mărginită, deoarece |sin(x)| ≤ 1."
    },
    {
        "id": "asimptote_functie",
        "descriere": r"Asimptote, asimptotă verticală, orizontală, oblică, comportament la infinit.",
        "hint": r"ATENȚIE: Asimptotă verticală: x = a dacă lim(x→a) f(x) = ±∞. Asimptotă orizontală: y = L dacă lim(x→±∞) f(x) = L. Asimptotă oblică: y = mx + n unde m = lim(x→∞) f(x)/x și n = lim(x→∞) [f(x) - mx]."
    },
    {
        "id": "teorema_valorilor_intermediare",
        "descriere": r"Teorema lui Darboux, valori intermediare, f(a) și f(b) cu semn opus, rădăcini.",
        "hint": r"ATENȚIE: Dacă f este continuă pe [a,b] și f(a)·f(b) < 0 (semne opuse), atunci EXISTĂ cel puțin un c ∈ (a,b) cu f(c) = 0. Această teoremă garantează existența rădăcinii, dar nu unicitatea!"
    },
    {
        "id": "limite_laterale",
        "descriere": r"Limite laterale, limita la stânga, limita la dreapta, lim x->a-, lim x->a+.",
        "hint": r"ATENȚIE: Limita globală lim(x→a) f(x) există NUMAI dacă ambele limite laterale există și sunt egale: lim(x→a⁻) f(x) = lim(x→a⁺) f(x). Dacă limitele laterale sunt diferite, limita globală NU există."
    },

    # ================================================================
    # SECȚIUNEA 4: ANALIZĂ MATEMATICĂ – DERIVATE
    # ================================================================

    {
        "id": "derivata_compusa_chain_rule",
        "descriere": r"Derivata funcției compuse, chain rule, derivata lui f(g(x)).",
        "hint": r"ATENȚIE: Derivata funcției compuse f(g(x)) este f'(g(x)) · g'(x). Nu uita să înmulțești cu derivata funcției interioare! Aceasta este o greșeală frecventă în cazul (sin(x²))' = cos(x²) · 2x, nu doar cos(x²)."
    },
    {
        "id": "derivata_functiei_inverse",
        "descriere": r"Derivata funcției inverse, (f⁻¹)'(x), derivata lui arcsin, arccos, arctan.",
        "hint": r"ATENȚIE: (arcsin(x))' = 1/√(1-x²) definit pe (-1,1). (arccos(x))' = -1/√(1-x²). (arctan(x))' = 1/(1+x²) definit pe ℝ. Observă că derivata lui arccos are semnul MINUS față de arcsin!"
    },
    {
        "id": "regula_produsului_derivata",
        "descriere": r"Derivata unui produs de funcții, (f·g)', regula Leibniz.",
        "hint": r"ATENȚIE: (f·g)' = f'·g + f·g'. Nu confunda cu (f·g)' = f'·g'! Aceasta este o greșeală clasică. Derivata produsului NU este produsul derivatelor."
    },
    {
        "id": "regula_catului_derivata",
        "descriere": r"Derivata unui câț de funcții, (f/g)', derivata fracției.",
        "hint": r"ATENȚIE: (f/g)' = (f'·g - f·g') / g². Ordinea din numărător contează: mai întâi f'g, apoi scădem fg'. Nu uita să ridici numitorul la pătrat! Asigură-te că g(x) ≠ 0 pe intervalul de definiție."
    },
    {
        "id": "monotonie_si_extremele_functiei",
        "descriere": r"Monotonia funcției, puncte de extrem, maxim local, minim local, derivata prima.",
        "hint": r"ATENȚIE: f'(x) > 0 ⟹ f crescătoare, f'(x) < 0 ⟹ f descrescătoare. Dacă f'(x₀) = 0, x₀ este CANDIDAT la extrem. Verifică schimbarea semnului lui f': dacă trece de la + la -, este maxim local; de la - la +, minim local. Dacă semnul nu se schimbă, NU este extrem!"
    },
    {
        "id": "concavitate_convexitate_derivata_secunda",
        "descriere": r"Concavitate, convexitate, punct de inflexiune, derivata a doua, f''(x).",
        "hint": r"ATENȚIE: f''(x) > 0 ⟹ funcția este convexă (curbată în sus). f''(x) < 0 ⟹ concavă (curbată în jos). Punctul de inflexiune apare unde f''(x) = 0 ȘI f'' își schimbă semnul. f''(x₀) = 0 singur nu garantează inflexiune!"
    },
    {
        "id": "teorema_lui_lagrange_valoarea_medie",
        "descriere": r"Teorema valorii medii, teorema lui Lagrange, f'(c) = (f(b)-f(a))/(b-a).",
        "hint": r"ATENȚIE: Teorema lui Lagrange garantează existența unui c ∈ (a,b) cu f'(c) = (f(b)-f(a))/(b-a), DAR NUMAI dacă f este continuă pe [a,b] și derivabilă pe (a,b). Verifică condițiile înainte de aplicare!"
    },
    {
        "id": "regula_lhopital_aplicare",
        "descriere": r"Regula lui l'Hôpital, forme nedeterminate 0·∞, ∞-∞, 0^0, 1^∞, ∞^0.",
        "hint": r"ATENȚIE: Formele 0·∞, ∞-∞, 0^0, 1^∞, ∞^0 NU sunt direct de tipul 0/0 sau ∞/∞. Trebuie să le transformi: 0·∞ → 0/(1/∞) sau ∞/(1/0). Formele cu puteri (0^0, 1^∞) se transformă via logaritm: lim f^g = e^(lim g·ln(f))."
    },
    {
        "id": "derivabilitate_implica_continuitate",
        "descriere": r"Relația dintre derivabilitate și continuitate, funcție derivabilă vs. funcție continuă.",
        "hint": r"ATENȚIE: Dacă o funcție este derivabilă în x₀, atunci este și continuă în x₀. Reciproca NU este adevărată: o funcție poate fi continuă dar nediferenţiabilă (ex: |x| în 0). La demonstrații, nu confunda cele două proprietăți!"
    },
    {
        "id": "optimizare_cu_constrangeri",
        "descriere": r"Probleme de optimizare, maxim și minim pe un interval închis, capete de interval.",
        "hint": r"ATENȚIE: Pe un interval ÎNCHIS [a,b], valoarea maximă/minimă poate fi atinsă la un punct interior (unde f'=0) SAU la capetele intervalului a sau b. Calculează f în TOATE punctele critice și în capete, apoi compară!"
    },

    # ================================================================
    # SECȚIUNEA 5: ANALIZĂ MATEMATICĂ – INTEGRALE
    # ================================================================

    {
        "id": "integrala_impara_simetric",
        "descriere": r"Integrale definite, funcții impare, interval simetric, integrală de la -a la a.",
        "hint": r"ATENȚIE: Integrala definită a unei funcții IMPARE (f(-x) = -f(x)) pe un interval simetric [-a, a] este ZERO. Integrala unei funcții PARE (f(-x) = f(x)) pe [-a,a] este dublul integralei de la 0 la a."
    },
    {
        "id": "constanta_de_integrare",
        "descriere": r"Integrală nedefinită, primitivă, constanta C, antiderivată.",
        "hint": r"ATENȚIE: Orice integrală nedefinită (primitivă) trebuie să conțină constanta de integrare +C la final. Fără +C, răspunsul este incomplet. Familia de primitive diferă prin această constantă arbitrară."
    },
    {
        "id": "integrare_prin_parti",
        "descriere": r"Integrarea prin părți, ∫u·dv = u·v - ∫v·du, formula Green-Gauss.",
        "hint": r"ATENȚIE: La integrarea prin părți ∫u·dv = u·v - ∫v·du, alegerea corectă a lui u și dv este crucială. Regula LIATE: Logaritmi, Inversă trigonometrică, Algebrică, Trigonometrică, Exponențială – alege u în această ordine de prioritate."
    },
    {
        "id": "schimbare_variabila_integrare",
        "descriere": r"Schimbare de variabilă la integrare, substituție, ∫f(g(x))·g'(x)dx.",
        "hint": r"ATENȚIE: La schimbarea de variabilă t = g(x), nu uita să schimbi și diferențiala: dt = g'(x)dx. La integralele DEFINITE, schimbă și limitele de integrare conform substituției noi! Nu reveni la variabila originală dacă ai schimbat limitele."
    },
    {
        "id": "teorema_fundamentala_calculului",
        "descriere": r"Teorema fundamentală a calculului, derivata integralei, F'(x) = f(x).",
        "hint": r"ATENȚIE: Dacă F(x) = ∫[a,x] f(t)dt, atunci F'(x) = f(x). Dacă limita superioară este o funcție g(x), aplică chain rule: d/dx ∫[a,g(x)] f(t)dt = f(g(x)) · g'(x). Dacă ambele limite depind de x, descompune integrala!"
    },
    {
        "id": "integrala_improprie_convergenta",
        "descriere": r"Integrala improprie, convergența integralei, ∫ de la a la infinit.",
        "hint": r"ATENȚIE: O integrală improprie ∫[a,∞) f(x)dx converge NUMAI dacă lim(b→∞) ∫[a,b] f(x)dx există și este finit. Exemplu clasic: ∫[1,∞) 1/x^p dx converge pentru p > 1 și diverge pentru p ≤ 1."
    },
    {
        "id": "arie_suprafata_integrala",
        "descriere": r"Aria unei suprafețe plane, integrala definită, aria dintre două curbe.",
        "hint": r"ATENȚIE: Aria dintre curbele f(x) și g(x) pe [a,b] este ∫[a,b] |f(x) - g(x)|dx. Modulul este ESENȚIAL dacă curbele se intersectează pe interval! Găsește punctele de intersecție și calculează integrala pe fiecare subinterval separat."
    },
    {
        "id": "integrala_functii_trigonometrice_puteri",
        "descriere": r"Integrala puterilor funcțiilor trigonometrice, ∫sin^n(x)dx, ∫cos^n(x)dx.",
        "hint": r"ATENȚIE: Pentru ∫sin^n(x)dx sau ∫cos^n(x)dx: dacă n este impar, separă un factor și folosește identitatea pitagoreică. Dacă n este par, folosește formulele de coborâre a puterii: sin²x = (1-cos2x)/2, cos²x = (1+cos2x)/2."
    },

    # ================================================================
    # SECȚIUNEA 6: COMBINATORICĂ ȘI PROBABILITATE
    # ================================================================

    {
        "id": "conditii_combinari_aranjamente",
        "descriere": r"Combinatorică, combinări, aranjamente, permutări, factorial, C(n,k), A(n,k).",
        "hint": r"ATENȚIE: Pentru combinări și aranjamente, n și k trebuie să fie numere naturale (≥ 0), iar n ≥ k. Orice soluție fracționară sau negativă se respinge. C(n,0) = C(n,n) = 1. Dacă k > n, C(n,k) = 0."
    },
    {
        "id": "suma_progresie_geometrica_infinita",
        "descriere": r"Suma unei progresii geometrice infinite, serii convergente, suma de la 1 la infinit.",
        "hint": r"ATENȚIE: Suma progresiei geometrice infinite S = a₁/(1-q) este validă NUMAI dacă |q| < 1. Dacă |q| ≥ 1, seria diverge și nu are sumă finită."
    },
    {
        "id": "probabilitate_conditionata",
        "descriere": r"Probabilitate condiționată, P(A|B), independența evenimentelor.",
        "hint": r"ATENȚIE: P(A|B) = P(A∩B) / P(B), NUMAI dacă P(B) > 0. Două evenimente sunt independente dacă P(A∩B) = P(A)·P(B). Nu confunda independența cu incompatibilitatea: evenimentele incompatibile (P(A∩B)=0) sunt de obicei DEPENDENTE!"
    },
    {
        "id": "formula_lui_bayes",
        "descriere": r"Teorema lui Bayes, probabilitate a posteriori, probabilitate totală.",
        "hint": r"ATENȚIE: Formula lui Bayes: P(Hₖ|A) = P(Hₖ)·P(A|Hₖ) / Σ P(Hᵢ)·P(A|Hᵢ). Asigură-te că ipotezele Hᵢ formează o partiție a spațiului (sunt mutual exclusive și exhaustive). Suma probabilităților lor trebuie să fie 1."
    },
    {
        "id": "distributia_binomiala",
        "descriere": r"Distribuție binomială, probabilitate de k succese din n încercări, B(n,p).",
        "hint": r"ATENȚIE: P(X=k) = C(n,k)·p^k·(1-p)^(n-k). Condiție: n încercări INDEPENDENTE cu ACEEAȘI probabilitate de succes p. Dacă probabilitatea se schimbă de la o încercare la alta, distribuția binomială nu se aplică!"
    },
    {
        "id": "principiul_cutiei_pigeonhole",
        "descriere": r"Principiul cutiei (Pigeonhole), n+1 obiecte în n cutii, cel puțin o cutie cu 2.",
        "hint": r"ATENȚIE: Dacă distribui n+1 obiecte în n cutii, cel puțin o cutie conține cel puțin 2 obiecte. Generalizare: dacă distribui k·n+1 obiecte în n cutii, cel puțin o cutie conține cel puțin k+1 obiecte. Identifică corect 'obiectele' și 'cutiile'."
    },
    {
        "id": "binomul_lui_newton",
        "descriere": r"Binomul lui Newton, (a+b)^n, coeficienți binomiali, triunghiul lui Pascal.",
        "hint": r"ATENȚIE: (a+b)^n = Σ C(n,k)·a^(n-k)·b^k pentru k=0,...,n. Termenul general este T_{k+1} = C(n,k)·a^(n-k)·b^k. Suma tuturor coeficienților este 2^n. Nu confunda termenul de rang k+1 cu termenul de rang k!"
    },
    {
        "id": "inductie_matematica",
        "descriere": r"Inducție matematică, demonstrație prin inducție, pasul de bază și pasul inductiv.",
        "hint": r"ATENȚIE: La demonstrația prin inducție: (1) verifică baza (de obicei n=1 sau n=0), (2) presupune că propoziția este adevărată pentru n=k (ipoteza de inducție), (3) demonstrează pentru n=k+1 FOLOSIND ipoteza. Ambii pași sunt obligatorii!"
    },

    # ================================================================
    # SECȚIUNEA 7: GEOMETRIE ANALITICĂ ȘI VECTORI
    # ================================================================

    {
        "id": "distanta_punct_dreapta",
        "descriere": r"Distanța de la un punct la o dreaptă, dreapta ax+by+c=0, punct (x0,y0).",
        "hint": r"ATENȚIE: Distanța de la punctul (x₀,y₀) la dreapta ax+by+c=0 este d = |ax₀+by₀+c| / √(a²+b²). Nu uita modulul la numărător și radicalul la numitor! Semnul numărătorului fără modul indică de ce parte a dreptei se află punctul."
    },
    {
        "id": "conditie_perpendicularitate_paralelism",
        "descriere": r"Perpendicularitate și paralelism între drepte, pante, coeficienți directori.",
        "hint": r"ATENȚIE: Două drepte cu pantele m₁ și m₂ sunt paralele dacă m₁ = m₂ și perpendiculare dacă m₁·m₂ = -1. Dacă una din drepte este verticală (pantă nedefinită), tratează cazul separat! O dreaptă verticală este perpendiculară pe orice dreaptă orizontală."
    },
    {
        "id": "produsul_scalar_vectori",
        "descriere": r"Produsul scalar a doi vectori, a·b = |a||b|cos(θ), componente.",
        "hint": r"ATENȚIE: Produsul scalar a·b = a₁b₁ + a₂b₂ + a₃b₃ = |a|·|b|·cos(θ). Doi vectori sunt PERPENDICULARI dacă și numai dacă produsul lor scalar este 0. Produsul scalar este COMUTATIV: a·b = b·a."
    },
    {
        "id": "produsul_vectorial",
        "descriere": r"Produsul vectorial, a×b, vectorul rezultant perpendicular pe ambii.",
        "hint": r"ATENȚIE: Produsul vectorial a×b este PERPENDICULAR pe ambii vectori a și b. |a×b| = |a|·|b|·sin(θ) reprezintă aria paralelogramului construit pe a și b. Produsul vectorial NU este comutativ: a×b = -(b×a)!"
    },
    {
        "id": "ecuatia_cercului",
        "descriere": r"Ecuația cercului, centru și rază, (x-a)^2 + (y-b)^2 = r^2.",
        "hint": r"ATENȚIE: Ecuația generală a cercului x²+y²+Dx+Ey+F=0 reprezintă un cerc REAL numai dacă r² = (D/2)²+(E/2)²-F > 0. Dacă r² = 0, este un punct. Dacă r² < 0, mulțimea este vidă. Calculează r² înainte de a concluziona!"
    },
    {
        "id": "pozitia_punct_fata_de_cerc",
        "descriere": r"Poziția unui punct față de un cerc, interior, exterior, pe cerc.",
        "hint": r"ATENȚIE: Fie cercul cu centrul O și raza r, și punctul P. Dacă |OP| < r, P este în INTERIORUL cercului. Dacă |OP| = r, P este PE cerc. Dacă |OP| > r, P este în EXTERIORUL cercului. Calculează distanța și comparo cu raza!"
    },
    {
        "id": "tangenta_la_cerc",
        "descriere": r"Tangenta la un cerc dintr-un punct exterior, numărul de tangente.",
        "hint": r"ATENȚIE: Dintr-un punct exterior unui cerc se pot duce EXACT 2 tangente. Dintr-un punct de pe cerc, exact 1 tangentă. Dintr-un punct interior, niciuna. Ecuația tangentei în punctul (x₀,y₀) la cercul x²+y²=r² este x·x₀ + y·y₀ = r²."
    },
    {
        "id": "conice_tipuri",
        "descriere": r"Conice, elipsă, parabolă, hiperbolă, ecuație generală de gradul 2.",
        "hint": r"ATENȚIE: Ecuația generală Ax²+Bxy+Cy²+Dx+Ey+F=0 descrie: elipsă dacă B²-4AC < 0, parabolă dacă B²-4AC = 0, hiperbolă dacă B²-4AC > 0. Calculează discriminantul pentru a identifica tipul de conică înainte de alte calcule."
    },

    # ================================================================
    # SECȚIUNEA 8: GEOMETRIE ÎN SPAȚIU ȘI GEOMETRIE PLANĂ
    # ================================================================

    {
        "id": "teorema_lui_pitagora_spatiu",
        "descriere": r"Teorema lui Pitagora în 3D, diagonala unui paralelipiped, distanța în spațiu.",
        "hint": r"ATENȚIE: Distanța dintre punctele (x₁,y₁,z₁) și (x₂,y₂,z₂) este √((x₂-x₁)²+(y₂-y₁)²+(z₂-z₁)²). Diagonala unui paralelipiped dreptunghic cu laturile a,b,c este d = √(a²+b²+c²). Nu confunda cu diagonala feței (2D)!"
    },
    {
        "id": "aria_triunghiului_determinant",
        "descriere": r"Aria unui triunghi cu vârfuri date prin coordonate, formula cu determinant.",
        "hint": r"ATENȚIE: Aria triunghiului cu vârfurile A(x₁,y₁), B(x₂,y₂), C(x₃,y₃) este |det([x₂-x₁, y₂-y₁; x₃-x₁, y₃-y₁])| / 2. Modulul este ESENȚIAL (aria este pozitivă). Dacă aria = 0, punctele sunt coliniare!"
    },
    {
        "id": "unghi_poliedru_diedru",
        "descriere": r"Unghiuri în geometria spațiului, unghi diedru, unghi la poliedre, proiecție.",
        "hint": r"ATENȚIE: Unghiul diedru dintre două planuri se calculează ca unghiul dintre normalele lor sau ca unghiul dintre liniile perpendiculare pe muchia comună, trasate în fiecare plan. Folosește produsul scalar al normalelor: cos(θ) = |n₁·n₂| / (|n₁|·|n₂|)."
    },
    {
        "id": "volume_formule",
        "descriere": r"Volume, volum poliedru, sferă, con, piramidă, cilindru.",
        "hint": r"ATENȚIE: Volum sferă = (4/3)πr³. Volum con = (1/3)πr²h. Volum piramidă = (1/3)·Arie_baza·h. Volum cilindru = πr²h. Atenție la deosebire: factorul 1/3 apare la con ȘI piramidă, dar NU la cilindru!"
    },
    {
        "id": "teorema_sinusurilor",
        "descriere": r"Teorema sinusurilor, a/sin(A) = b/sin(B) = c/sin(C) = 2R.",
        "hint": r"ATENȚIE: Teorema sinusurilor: a/sin(A) = b/sin(B) = c/sin(C) = 2R, unde R este raza cercului circumscris. Folosind această teoremă, un unghi obținut din arcsin poate fi OBTUZ sau ASCUȚIT – verifică ambele posibilități (sin(x) = sin(π-x))!"
    },
    {
        "id": "teorema_cosinusurilor",
        "descriere": r"Teorema cosinusurilor, c^2 = a^2 + b^2 - 2ab·cos(C), generalizare Pitagora.",
        "hint": r"ATENȚIE: Teorema cosinusurilor c² = a²+b²-2ab·cos(C) generalizează Pitagora. Dacă cos(C) < 0 (unghiul C este obtuz), termenul -2ab·cos(C) devine pozitiv, deci c² > a²+b². Verifică tipul triunghiului (ascuțitunghic/obtuzunghic) din semnul cosinusului."
    },
    {
        "id": "locul_geometric",
        "descriere": r"Loc geometric, mulțimea punctelor care satisfac o proprietate, cerc, parabolă.",
        "hint": r"ATENȚIE: Un loc geometric este mulțimea TUTUROR punctelor cu o proprietate dată, nu doar câteva. La determinarea lui, demonstrează AMBELE incluziuni: (1) orice punct din loc satisface proprietatea, (2) orice punct cu proprietatea aparține locului."
    },

    # ================================================================
    # SECȚIUNEA 9: TEORIA NUMERELOR ȘI ALGEBRĂ ABSTRACTĂ
    # ================================================================

    {
        "id": "congruente_modulo",
        "descriere": r"Congruențe modulo, a ≡ b (mod n), aritmetică modulară, restul împărțirii.",
        "hint": r"ATENȚIE: a ≡ b (mod n) înseamnă că n | (a-b). La calcule cu congruențe poți aduna, scădea și înmulți, DAR împărțirea necesită existența inversului modular. Nu împărți direct în congruențe – înmulțește cu inversul lui a (dacă gcd(a,n)=1)."
    },
    {
        "id": "teorema_lui_fermat_mic",
        "descriere": r"Mica teoremă a lui Fermat, a^p ≡ a (mod p), p număr prim.",
        "hint": r"ATENȚIE: Mica teoremă Fermat: dacă p este prim și gcd(a,p)=1, atunci a^(p-1) ≡ 1 (mod p). Utilă pentru calculul puterilor mari modulo un prim. Atenție: dacă p nu este prim, teorema NU se aplică!"
    },
    {
        "id": "functia_lui_euler",
        "descriere": r"Funcția lui Euler φ(n), numărul de întregi coprimi cu n, teorema Euler.",
        "hint": r"ATENȚIE: Teorema lui Euler: a^φ(n) ≡ 1 (mod n), valabilă când gcd(a,n)=1. φ(p) = p-1 pentru p prim. φ(p^k) = p^(k-1)·(p-1). φ este multiplicativă: φ(mn) = φ(m)φ(n) dacă gcd(m,n)=1."
    },
    {
        "id": "sirul_fibonacci_proprietati",
        "descriere": r"Șirul lui Fibonacci, F(n) = F(n-1) + F(n-2), proprietăți, formula lui Binet.",
        "hint": r"ATENȚIE: Termenul general al șirului Fibonacci prin formula lui Binet: F(n) = (φ^n - ψ^n)/√5, unde φ=(1+√5)/2 (secțiunea de aur) și ψ=(1-√5)/2. Proprietate: orice al treilea termen Fibonacci este par. gcd(F(m),F(n)) = F(gcd(m,n))."
    },

    # ================================================================
    # SECȚIUNEA 10: ECUAȚII DIFERENȚIALE ȘI ALGEBRĂ LINIARĂ
    # ================================================================

    {
        "id": "ecuatie_diferentiala_ordinul_1_separabile",
        "descriere": r"Ecuații diferențiale, variabile separabile, dy/dx = f(x)g(y).",
        "hint": r"ATENȚIE: La separarea variabilelor, nu uita că dacă g(y) = 0 poate exista o soluție particulară y = constantă. Această soluție singulară s-ar putea să nu fie cuprinsă în soluția generală. Verifică separat dacă g(y) = 0 dă soluții valide."
    },
    {
        "id": "ecuatie_diferentiala_liniara_ordinul_2",
        "descriere": r"Ecuație diferențială liniară de ordinul 2 cu coeficienți constanți.",
        "hint": r"ATENȚIE: Soluția generală a ecuației ay''+by'+cy=0 depinde de discriminantul Δ=b²-4ac: dacă Δ>0, două rădăcini reale distincte; dacă Δ=0, o rădăcină reală dublă; dacă Δ<0, rădăcini complexe conjugate. Fiecare caz dă un tip diferit de soluție generală!"
    },
    {
        "id": "valori_proprii_vectori_proprii",
        "descriere": r"Valori proprii, vectori proprii, diagonalizarea matricelor, ecuația caracteristică.",
        "hint": r"ATENȚIE: Valorile proprii se găsesc din ecuația caracteristică det(A - λI) = 0. Pentru fiecare valoare proprie λ, vectorii proprii se găsesc rezolvând (A-λI)v=0. Un vector propriu NU poate fi vectorul zero! Verifică că v ≠ 0."
    },
    {
        "id": "rang_matrice_sistem",
        "descriere": r"Rangul unei matrice, teorema Kronecker-Capelli, compatibilitatea sistemelor.",
        "hint": r"ATENȚIE: Teorema Kronecker-Capelli: sistemul Ax=b este compatibil DACĂ ȘI NUMAI DACĂ rang(A) = rang(A|b). Dacă rang(A) = rang(A|b) = n (nr. necunoscute), soluția este unică. Dacă rang(A) = rang(A|b) < n, sunt infinit de soluții. Dacă rangurile diferă, sistemul este incompatibil."
    },
    {
        "id": "transformari_liniare_nucleu_imagine",
        "descriere": r"Transformări liniare, nucleul (ker), imaginea (Im), teorema rang-nulitate.",
        "hint": r"ATENȚIE: Teorema rang-nulitate: dim(ker(T)) + dim(Im(T)) = dim(spațiu sursă). dim(ker(T)) se numește nulitate, dim(Im(T)) se numește rang. Transformarea este injectivă DACĂ ȘI NUMAI DACĂ ker(T) = {0} (nulitate = 0)."
    },

    # ================================================================
    # SECȚIUNEA 11: SERII ȘI ȘIRURI
    # ================================================================

    {
        "id": "convergenta_serie_termenul_general",
        "descriere": r"Convergența unei serii, termenul general, condiție necesară de convergență.",
        "hint": r"ATENȚIE: Condiție NECESARĂ (nu suficientă) de convergență: dacă seria Σaₙ converge, atunci aₙ → 0. Reciproca este FALSĂ: seria armonică Σ(1/n) are termenul general → 0 dar DIVERGE. Nu confunda condiția necesară cu cea suficientă!"
    },
    {
        "id": "criteriul_raportului_dalembert",
        "descriere": r"Criteriul raportului (D'Alembert), lim |a_{n+1}/a_n| = L, convergența seriei.",
        "hint": r"ATENȚIE: Criteriul raportului D'Alembert: fie L = lim|a_{n+1}/a_n|. Dacă L < 1, seria converge absolut. Dacă L > 1, seria diverge. Dacă L = 1, criteriul este INCONCLUZIV – trebuie folosit alt criteriu (Raabe, Gauss, comparație etc.)."
    },
    {
        "id": "criteriul_comparatiei_serii",
        "descriere": r"Criteriul comparației pentru serii, serie mai mică decât una convergentă.",
        "hint": r"ATENȚIE: Dacă 0 ≤ aₙ ≤ bₙ pentru n suficient de mare: dacă Σbₙ converge, atunci Σaₙ converge; dacă Σaₙ diverge, atunci Σbₙ diverge. Criteriul funcționează NUMAI pentru serii cu termeni POZITIVI (sau nenegativi)!"
    },
    {
        "id": "seria_taylor_maclaurin",
        "descriere": r"Seria Taylor, seria Maclaurin, dezvoltarea în serie de puteri a unei funcții.",
        "hint": r"ATENȚIE: Seria Taylor a lui f în jurul lui a este Σ f^(n)(a)/n! · (x-a)^n. Converge NUMAI în raza de convergență R. Funcția = seria ei Taylor NUMAI dacă restul Rₙ(x) → 0. Nu orice funcție infinit derivabilă este egală cu seria sa Taylor!"
    },
    {
        "id": "sir_cauchy_convergenta",
        "descriere": r"Șir Cauchy, criteriu Cauchy de convergență, șir convergent implică șir Cauchy.",
        "hint": r"ATENȚIE: Un șir convergent este MEREU Cauchy. Reciproca este adevărată în ℝ (completitudinea lui ℝ), dar NU în toate spațiile metrice. Un șir Cauchy în ℝ converge ÎNTOTDEAUNA."
    },

    # ================================================================
    # SECȚIUNEA 12: STATISTICĂ ȘI TEORIA MĂSURII
    # ================================================================

    {
        "id": "media_versus_mediana",
        "descriere": r"Media aritmetică vs. mediana unui șir de date, statistică descriptivă.",
        "hint": r"ATENȚIE: Media este sensibilă la valorile extreme (outlieri), pe când mediana nu este. Dacă distribuția este asimetrică sau conține valori anormale, mediana este un indicator mai reprezentativ al 'tendinței centrale' decât media."
    },
    {
        "id": "varianta_dispersie_deviatia_standard",
        "descriere": r"Varianță, dispersie, deviație standard, σ², σ, calculul împrăștierii datelor.",
        "hint": r"ATENȚIE: Varianța populației σ² = Σ(xᵢ - μ)²/N, iar varianța EȘANTIONULUI s² = Σ(xᵢ - x̄)²/(n-1) (cu n-1, nu n!). Împărțirea la n-1 în loc de n este corecția Bessel pentru a obține un estimator nedeplasat. Nu le confunda!"
    },
    {
        "id": "corelatie_vs_cauzalitate",
        "descriere": r"Corelație și cauzalitate, coeficient Pearson, relație statistică.",
        "hint": r"ATENȚIE: Corelația STATISTICĂ (chiar și puternică, cu r aproape de ±1) NU implică CAUZALITATE! Două variabile pot fi corelate din cauza unui factor comun (variabilă confundatoare) sau din pură coincidență. Nu trage concluzii cauzale din date observaționale fără analiză suplimentară."
    },
    {
        "id": "intervalul_de_incredere",
        "descriere": r"Interval de încredere, nivel de semnificație, probabilitate de acoperire.",
        "hint": r"ATENȚIE: Un interval de încredere de 95% NU înseamnă că parametrul populației se află în interval cu probabilitate 95%. Înseamnă că PROCEDURA de construire a intervalului produce intervale care conțin parametrul în 95% din cazuri. Parametrul fie este, fie nu este în intervalul specific calculat."
    },

    # ================================================================
    # SECȚIUNEA 13: LOGICĂ MATEMATICĂ ȘI MULȚIMI
    # ================================================================

    {
        "id": "negarea_cuantificatorilor",
        "descriere": r"Negarea propoziților cu cuantificatori, negarea lui 'pentru toți' și 'există'.",
        "hint": r"ATENȚIE: Negarea lui '∀x, P(x)' este '∃x, ¬P(x)'. Negarea lui '∃x, P(x)' este '∀x, ¬P(x)'. Cuantificatorul se schimbă și propoziția se neagă! Greșeală frecventă: scrierea negării lui '∀x, P(x)' ca '∀x, ¬P(x)' – aceasta înseamnă ceva complet diferit."
    },
    {
        "id": "demonstratie_prin_contradictie",
        "descriere": r"Demonstrație prin reducere la absurd, demonstrație indirectă, contra-pozitivă.",
        "hint": r"ATENȚIE: La demonstrația prin contradicție, presupui că NEGAREA concuziei este adevărată și derivezi o contradicție (o propoziție falsă). Contrapoziția lui 'P ⟹ Q' este '¬Q ⟹ ¬P' și este logic echivalentă cu implicația originală. Nu confunda cu contrariul sau conversa!"
    },
    {
        "id": "operatii_cu_multimi",
        "descriere": r"Operații cu mulțimi, reuniune, intersecție, diferență, complement, legile lui De Morgan.",
        "hint": r"ATENȚIE: Legile lui De Morgan: complementul reuniunii = intersecția complementelor: (A∪B)ᶜ = Aᶜ∩Bᶜ, iar complementul intersecției = reuniunea complementelor: (A∩B)ᶜ = Aᶜ∪Bᶜ. Acestea sunt esențiale în teoria mulțimilor și logică."
    },
    {
        "id": "cardinalul_multimilor",
        "descriere": r"Cardinalul unei mulțimi, mulțimi infinite, numărabilitate, mulțimea putere.",
        "hint": r"ATENȚIE: |A∪B| = |A| + |B| - |A∩B| (principiul includere-excludere). Cardinalul mulțimii putere P(A) este 2^|A|. Există infinit de 'tipuri' de infinit (Cantor): ℕ și ℤ sunt numărabile, dar ℝ este nenumărabil (mai 'mare')."
    },

    # ================================================================
    # SECȚIUNEA 14: FUNCȚII SPECIALE ȘI ALTE REGULI
    # ================================================================

    {
        "id": "functia_floor_ceiling",
        "descriere": r"Funcția parte întreagă, floor, ceiling, [x], ⌊x⌋, ⌈x⌉.",
        "hint": r"ATENȚIE: ⌊x⌋ (floor) este cel mai mare întreg ≤ x. ⌈x⌉ (ceiling) este cel mai mic întreg ≥ x. Atenție: ⌊-2.3⌋ = -3, NU -2! Pentru negativi, floor 'coboară' mai mult. De asemenea, ⌊x⌋ = x dacă și numai dacă x ∈ ℤ."
    },
    {
        "id": "functia_signum",
        "descriere": r"Funcția semn (signum), sgn(x), semnul unui număr real.",
        "hint": r"ATENȚIE: sgn(x) = 1 dacă x > 0, sgn(x) = 0 dacă x = 0, sgn(x) = -1 dacă x < 0. Proprietate: x = sgn(x)·|x| pentru orice x ∈ ℝ. Nu confunda: sgn(0) = 0, nu ±1."
    },
    {
        "id": "functia_exponentiala_proprietati",
        "descriere": r"Funcția exponențială, e^x, proprietăți, e^x > 0 pentru orice x real.",
        "hint": r"ATENȚIE: e^x > 0 pentru ORICE x ∈ ℝ – funcția exponențială este MEREU pozitivă, niciodată zero sau negativă. e^0 = 1. e^(a+b) = e^a · e^b. (e^a)^b = e^(ab). Nu confunda e^(a+b) cu e^a + e^b!"
    },
    {
        "id": "proprietati_logaritm_natural",
        "descriere": r"Proprietăți ale logaritmului natural ln(x), reguli de calcul.",
        "hint": r"ATENȚIE: ln(a·b) = ln(a) + ln(b), ln(a/b) = ln(a) - ln(b), ln(a^r) = r·ln(a). ATENȚIE CAPITALĂ: ln(a+b) ≠ ln(a) + ln(b)! Nu există o formulă simplă pentru logaritmul unei sume. ln(1) = 0, ln(e) = 1."
    },
    {
        "id": "schimbare_baza_logaritm",
        "descriere": r"Schimbarea bazei unui logaritm, log_a(b) = ln(b)/ln(a).",
        "hint": r"ATENȚIE: log_a(b) = log_c(b) / log_c(a) pentru orice bază c > 0, c ≠ 1. Caz special: log_a(b) = 1/log_b(a). Asigură-te că baza a > 0 și a ≠ 1, și argumentul b > 0 înainte de orice calcul."
    },
    {
        "id": "produsul_notabil_suma_cub",
        "descriere": r"Produse notabile, suma și diferența de cuburi, a^3 ± b^3.",
        "hint": r"ATENȚIE: a³+b³ = (a+b)(a²-ab+b²) și a³-b³ = (a-b)(a²+ab+b²). Factorul de gradul 2 (a²∓ab+b²) este IREDUCTIBIL în ℝ (discriminantul este negativ). Nu îl mai factoriza! Greșeală frecventă: scrierea a³+b³ = (a+b)³."
    },
    {
        "id": "regula_semnelor_descartes",
        "descriere": r"Regula semnelor Descartes, numărul de rădăcini pozitive/negative ale unui polinom.",
        "hint": r"ATENȚIE: Regula lui Descartes: numărul rădăcinilor reale POZITIVE ale polinomului P(x) este egal cu numărul schimbărilor de semn ale coeficienților SAU cu acel număr minus un număr par. Rădăcinile negative ale P(x) corespund rădăcinilor pozitive ale P(-x)."
    },
    {
        "id": "inegalitatea_cauchy_schwarz",
        "descriere": r"Inegalitatea Cauchy-Schwarz, (Σaᵢbᵢ)² ≤ (Σaᵢ²)(Σbᵢ²).",
        "hint": r"ATENȚIE: Inegalitatea Cauchy-Schwarz: (a₁b₁+a₂b₂+...+aₙbₙ)² ≤ (a₁²+...+aₙ²)(b₁²+...+bₙ²). Egalitatea are loc DACĂ ȘI NUMAI DACĂ vectorii (a₁,...,aₙ) și (b₁,...,bₙ) sunt proporționali (unul este scalar multiplu al celuilalt)."
    },
    {
        "id": "inegalitatea_triunghiului",
        "descriere": r"Inegalitatea triunghiului, |a+b| ≤ |a|+|b|, norma vectorilor.",
        "hint": r"ATENȚIE: Inegalitatea triunghiului: |a+b| ≤ |a|+|b|. Egalitatea are loc NUMAI când a și b au același semn (sau unul e zero). Versiune inversă: ||a|-|b|| ≤ |a-b|. Valabilă și pentru vectori și numere complexe!"
    },
    {
        "id": "functii_periodice_compuse",
        "descriere": r"Periodicitatea funcțiilor compuse, perioada funcției f(ax+b).",
        "hint": r"ATENȚIE: Dacă f(x) are perioada T, atunci f(ax+b) are perioada T/|a| (nu T!). Exemplu: sin(2x) are perioada π = 2π/2, nu 2π. La suma de funcții periodice, perioada rezultantă este LCM (CMMMC) al perioadelor, DACĂ acesta există."
    },
    {
        "id": "monotonie_functii_inverse",
        "descriere": r"Monotonia funcțiilor inverse, dacă f este crescătoare/descrescătoare, atunci f⁻¹...",
        "hint": r"ATENȚIE: Dacă f este STRICT MONOTONĂ (crescătoare sau descrescătoare) și continuă, atunci f⁻¹ există și are ACEEAȘI monotonie ca f. O funcție inversă a unei funcții crescătoare este tot crescătoare; a unei descrescătoare, tot descrescătoare."
    },
    {
        "id": "paritate_imparitate_functii",
        "descriere": r"Paritatea și imparitatea funcțiilor, f(-x) = f(x) sau f(-x) = -f(x).",
        "hint": r"ATENȚIE: O funcție este pară dacă f(-x) = f(x) pentru orice x din domeniu, și impară dacă f(-x) = -f(x). Domeniul trebuie să fie SIMETRIC față de 0. Suma/diferența a două funcții pare este pară; a două impare este impară; o pară cu o impară este în general nici pară, nici impară."
    },
    {
        "id": "proprietati_modul_complex",
        "descriere": r"Proprietăți ale modulului numerelor complexe, |z₁·z₂| = |z₁|·|z₂|.",
        "hint": r"ATENȚIE: |z₁·z₂| = |z₁|·|z₂| și |z₁/z₂| = |z₁|/|z₂|. ATENȚIE: |z₁+z₂| ≤ |z₁|+|z₂| (inegalitatea triunghiului pentru complexe). NU este adevărat că |z₁+z₂| = |z₁|+|z₂| în general!"
    },
    {
        "id": "formula_euler_totient",
        "descriere": r"Calculul funcției totient Euler pentru produse de numere prime, φ(p₁^a₁ · p₂^a₂ ...).",
        "hint": r"ATENȚIE: φ(n) = n · ∏(1 - 1/p) pentru toți p primi ce divid n. Exemplu: φ(12) = φ(2²·3) = 12·(1-1/2)·(1-1/3) = 12·1/2·2/3 = 4. Dacă n = p (prim), φ(p) = p-1. φ este multiplicativă doar pentru numere coprime!"
    },
{
        "id": "teorema_cayley_hamilton",
        "descriere": r"Teorema Cayley-Hamilton, polinomul caracteristic al unei matrice, A satisface propria ecuație caracteristică, p(A) = 0.",
        "hint": r"ATENȚIE: NU substitui direct matricea A în formula determinantului det(λI - A) = 0 în loc de λ — aceasta este o eroare fatală (eroarea substituției scalare directe). Coeficienții polinomului caracteristic trebuie calculați explicit, iar A se substituie în forma EXPANDATĂ a polinomului, termenul liber c₀ devenind c₀·I. Reducerea puterilor lui A la combinații liniare de puteri inferioare se face NUMAI după această substituție corectă."
    },
    {
        "id": "cercurile_gershgorin",
        "descriere": r"Localizarea valorilor proprii, cercuri Gershgorin, spectrul unei matrice, estimarea valorilor proprii fără calcul direct.",
        "hint": r"ATENȚIE: Teorema Gershgorin garantează că TOATE valorile proprii se află în REUNIUNEA cercurilor, NU că fiecare cerc conține exact o valoare proprie — un cerc poate fi complet gol sau poate conține mai multe. Dacă originea (0) este inclusă în vreun cerc, NU se poate garanta că matricea este inversabilă prin acest criteriu. Concluzia privind numărul de valori proprii dintr-un grup IZOLAT de cercuri necesară o analiză topologică suplimentară (deformare continuă)."
    },
    {
        "id": "teorema_ceva_menelaus",
        "descriere": r"Concurența cevienelor, coliniaritatea punctelor pe laturile unui triunghi, teorema lui Ceva, teorema lui Menelaus, rapoarte de segmente.",
        "hint": r"ATENȚIE: Teorema lui Menelaus IMPUNE utilizarea lungimilor ORIENTATE (cu semn). Dacă un punct se află pe extensia laturii în afara triunghiului, raportul său este NEGATIV. Ignorarea semnului duce la concluzii false de coliniaritate. La Teorema lui Ceva, produsul egal cu +1 poate indica și drepte PARALELE (concurente la infinit în geometria proiectivă), nu doar concurente afin — tratează cazul dreptelor paralele separat!"
    },
    {
        "id": "teorema_stewart",
        "descriere": r"Lungimea unei ceviane într-un triunghi, Teorema lui Stewart, relație dintre ceviană și laturile triunghiului, d²a + mna = b²m + c²n.",
        "hint": r"ATENȚIE: Produsele asociază segmentele cu laturile NEADIACENTE — b²m și c²n, unde m este segmentul de pe latura a adiacent vârfului B, iar n cel adiacent lui C. Inversarea asocierii b↔c produce rezultate complet eronate! Dacă punctul este pe EXTENSIA laturii (în afara triunghiului), unul din segmente m sau n devine negativ (lungime orientată), modificând ecuația. La bisectoare, combină cu Teorema Bisectoarei (b/c = n/m)."
    },
    {
        "id": "teorema_ptolemeu",
        "descriere": r"Patrulater inscriptibil, Teorema lui Ptolemeu, AC·BD = AB·CD + BC·AD, relație dintre diagonale și laturi.",
        "hint": r"ATENȚIE: Egalitatea Ptolemeu (AC·BD = AB·CD + BC·AD) este valabilă NUMAI pentru patrulatere INSCRIPTIBILE (ciclice). Pentru un patrulater general, relația devine INEGALITATE (Inegalitatea lui Ptolemeu): AC·BD ≤ AB·CD + BC·AD. Verifică ÎNTOTDEAUNA că cele 4 puncte sunt conciclice înainte de a aplica egalitatea! Confuzia patrulater general vs. inscriptibil este sursa principală de erori."
    },
    {
        "id": "formula_brahmagupta",
        "descriere": r"Aria unui patrulater inscriptibil, Formula lui Brahmagupta, K = sqrt((s-a)(s-b)(s-c)(s-d)), semiperimetru.",
        "hint": r"ATENȚIE: Formula Brahmagupta K = √[(s-a)(s-b)(s-c)(s-d)] este valabilă EXCLUSIV pentru patrulatere INSCRIPTIBILE (ciclice). Pentru un patrulater general, trebuie folosită Formula lui Bretschneider: K = √[(s-a)(s-b)(s-c)(s-d) - abcd·cos²(θ)], unde θ este jumătatea sumei unghiurilor opuse. Aplicarea Brahmagupta pe patrulatere non-ciclice SUPRAESTIMEAZĂ aria (presupune implicit θ=90°). Reține: configurația inscriptibilă maximizează aria pentru laturi fixe."
    },
    {
        "id": "teorema_pick",
        "descriere": r"Aria unui poligon cu vârfuri pe noduri de grilă întreagă, Teorema lui Pick, A = i + b/2 - 1, puncte interioare și de frontieră.",
        "hint": r"ATENȚIE: Parametrul b (puncte de frontieră) NU se calculează numărând doar vârfurile! Pe fiecare segment dintre vârfurile (x₁,y₁)-(x₂,y₂) există GCD(|x₂-x₁|, |y₂-y₁|) puncte pe frontieră (excluzând un capăt). Omiterea algoritmului GCD subestimează masiv b. De asemenea, formula A = i + b/2 - 1 este INVALIDĂ pentru poligoane cu auto-intersecții sau cu GĂURI interioare — în acele cazuri, constanta -1 trebuie înlocuită cu -χ/2 (caracteristica Euler a formei)."
    },
    {
        "id": "dreapta_euler_cercul_9_puncte",
        "descriere": r"Dreapta lui Euler, coliniaritatea ortocentrului H, centrului de greutate G și circumcentrului O, Cercul celor 9 puncte, raza R/2.",
        "hint": r"ATENȚIE: Într-un triunghi ECHILATERAL, punctele H, G și O coincid — Dreapta lui Euler devine nedefinită (degenerează la un punct). Centrul Cercului celor 9 puncte NU coincide cu centrul de greutate G, ci se află pe Dreapta lui Euler la mijlocul segmentului HO. Raza cercului celor 9 puncte este EXACT R/2 (jumătate din circumraza R). Relația de distanțe: HG = 2·GO (G împarte HO în raport 2:1)."
    },
    {
        "id": "teorema_desargues",
        "descriere": r"Geometrie proiectivă, perspectiva a două triunghiuri dintr-un punct sau o dreaptă, Configurația Desargues, punct perspector, perspectrix.",
        "hint": r"ATENȚIE: Teorema lui Desargues NU este valabilă în orice geometrie 2D! Ea eșuează în planele Non-Desarguesiene (ex: Planul Moulton). Coexistența axiomelor de incidență standard nu garantează Desargues. În planul real, demonstrația 2D coplanară necesită axiome adiționale — cea mai elegantă demonstrație 'evadează' în 3D (ridică triunghiurile în spațiu, aplică intersecția planelor, apoi proiectează înapoi). Teorema este condiția necesară pentru a putea construi un sistem de coordonate algebric coerent."
    },
    {
        "id": "teorema_chinezeasca_resturilor",
        "descriere": r"Teorema Chinezească a Resturilor, sistem de congruențe simultane, x ≡ aᵢ (mod nᵢ), soluție unică modulo N.",
        "hint": r"ATENȚIE: TCR garantează existența și unicitatea soluției NUMAI dacă modulele nᵢ sunt PAIRWISE COPRIME (GCD(nᵢ, nⱼ) = 1 pentru orice pereche). Dacă GCD > 1, sistemul poate fi incompatibil sau soluția nu mai este unică modulo produsul N, ci modulo LCM. Soluția eficientă se calculează prin Algoritmul lui Euclid Extins (coeficienții Bézout), reducând complexitatea de la O(N) la O(log N). Nu itera brut prin toate valorile de la 1 la N!"
    },
    {
        "id": "lte_lifting_the_exponent",
        "descriere": r"Lema LTE (Lifting The Exponent), evaluarea p-adică a lui xⁿ - yⁿ sau xⁿ + yⁿ, vₚ(xⁿ - yⁿ) = vₚ(x-y) + vₚ(n).",
        "hint": r"ATENȚIE: Lema LTE are forme DIFERITE pentru p impar și p=2! Pentru p IMPAR: dacă p∤x, p∤y și p|(x-y), atunci vₚ(xⁿ-yⁿ) = vₚ(x-y) + vₚ(n). Pentru p=2 cu n par: formula devine v₂(xⁿ-yⁿ) = v₂(x-y) + v₂(x+y) + v₂(n) - 1 (se adaugă v₂(x+y) și se scade 1!). Lema se INVALIDEAZĂ dacă x sau y este multiplu de p. Nu aplica formula pentru p=2 identică cu cea pentru p impar — diferența produce erori grave în olimpiade."
    },
    {
        "id": "criteriul_eisenstein",
        "descriere": r"Ireductibilitatea unui polinom cu coeficienți întregi peste Q, Criteriul lui Eisenstein, existența unui număr prim p cu condiții pe coeficienți.",
        "hint": r"ATENȚIE: Criteriul Eisenstein este o condiție SUFICIENTĂ, nu necesară! Dacă un polinom eșuează criteriul, NU înseamnă că este reductibil — poate fi ireductibil fără ca vreun prim să satisfacă condițiile. Soluție: aplică 'trucul translației' — dacă f(x) eșuează, testează f(x+a) pentru a=1,-1,2 etc. Ireductibilitatea este invariantă la translație, iar noua formă s-ar putea preta la Eisenstein. Exemplu clasic: polinomul ciclomic Φₚ(x) necesită evaluarea Φₚ(x+1) prin binomul lui Newton."
    },
    {
        "id": "sumele_newton_radacini",
        "descriere": r"Sumele lui Newton (Identitățile Newton), Sₖ = r₁ᵏ + r₂ᵏ + ... + rₙᵏ, suma puterilor rădăcinilor unui polinom fără a calcula rădăcinile.",
        "hint": r"ATENȚIE: La calculul Sₙ pentru n mai mare decât gradul polinomului, formula recurentă necesită EXTINDEREA ARTIFICIALĂ CU ZERO a coeficienților (coeficienții de grad superior gradului polinomului se tratează ca 0). Omiterea acestei extensii produce erori de index. De asemenea, metoda estimării rădăcinii dominante prin limita Sₖ/Sₖ₋₁ funcționează NUMAI dacă există o singură rădăcină dominantă reală. Perechile de rădăcini complexe conjugate de același modul produc oscilații divergente ale raportului, invalidând metoda."
    },
    {
        "id": "regula_leibniz_diferentiere_integrala",
        "descriere": r"Diferențierea sub semnul integralei, Regula Leibniz, derivata integralei parametrice cu limite variabile.",
        "hint": r"ATENȚIE: Formula completă este d/dx[∫ₐ₍ₓ₎^b₍ₓ₎ f(x,t)dt] = f(x,b(x))·b'(x) - f(x,a(x))·a'(x) + ∫ₐ^b ∂f/∂x dt. Nu arunca derivata doar sub integrală ignorând primii doi termeni de graniță — aceasta este validă NUMAI dacă limitele a și b sunt constante față de x! La integrale improprii (limite infinite), schimbul ordinii derivată-integrală necesită verificarea CONVERGENȚEI UNIFORME (M-testul Weierstrass sau Teorema Convergenței Dominate Lebesgue) — fără aceasta, rezultatul poate fi complet eronat."
    },
    {
        "id": "metoda_newton_raphson",
        "descriere": r"Metoda tangentelor Newton-Raphson, găsirea rădăcinilor numerice ale ecuațiilor, xₙ₊₁ = xₙ - f(xₙ)/f'(xₙ).",
        "hint": r"ATENȚIE: Metoda Newton-Raphson are două capcane majore: (1) DIVIZIUNEA PRIN ZERO — dacă f'(xₙ) = 0 la vreun pas iterativ (punct de extrem sau inflexiune cu tangentă orizontală), formula devine nedefinită și iterația diverge; (2) PUNCTUL DE START GREȘIT — dacă x₀ este ales în afara 'bazinului de convergență' al rădăcinii dorite, iterația poate oscila ciclic (x₁→x₂→x₁→...) sau poate converge spre o altă rădăcină decât cea dorită. Convergența pătratică (dublarea zecimalelor exacte per pas) este garantată NUMAI în vecinătatea rădăcinii."
    },
    {
        "id": "aproximarea_stirling",
        "descriere": r"Aproximarea lui Stirling pentru factoriale mari, n! ≈ √(2πn)·(n/e)ⁿ, analiza asimptotică O(n log n).",
        "hint": r"ATENȚIE: Seria de corecție Stirling (termenii adăugați pentru precizie suplimentară) este o serie ASIMPTOTICĂ DIVERGENTĂ — adăugarea prea multor termeni de corecție DEGRADEAZĂ precizia în loc s-o îmbunătățească! Există un număr optim de termeni (la care eroarea este minimă), după care eroarea CREȘTE exponențial. Pe valori mici (n < 10), formula de bază are erori semnificative. Limite utile: √(2πn)·(n/e)ⁿ ≤ n! ≤ e·n^(n+1/2)·e^(-n)."
    },
    {
        "id": "teorema_limitei_centrale",
        "descriere": r"Teorema Limitei Centrale (CLT), distribuția mediei eșantionului, convergența spre distribuție normală, variabile i.i.d.",
        "hint": r"ATENȚIE: Teorema Limitei Centrale presupune VARIANȚĂ FINITĂ a populației originale. Pentru distribuții 'heavy-tailed' (ex: Distribuția Cauchy, cu varianță infinită și medie incalculabilă), CLT NU se aplică, indiferent cât de mare este eșantionul! De asemenea, CLT necesită variabile INDEPENDENTE — eșantioanele corelate/dependente pot produce distribuții non-normale. Inegalitatea lui Bernoulli (1+x)^r ≥ 1+rx se aplică NUMAI pentru r≥1 și x≥-1; extinderea la r rațional negativ sau x<-1 produce erori."
    },
    {
        "id": "inegalitatea_jensen",
        "descriere": r"Inegalitatea lui Jensen, φ(E[X]) ≤ E[φ(X)] pentru funcții convexe, valoarea așteptată a unei transformări neliniare.",
        "hint": r"ATENȚIE: Inegalitatea Jensen (φ(E[X]) ≤ E[φ(X)]) este valabilă NUMAI dacă φ este CONVEXĂ (φ'' ≥ 0). Pentru funcții CONCAVE (φ'' ≤ 0), inegalitatea SE INVERSEAZĂ: φ(E[X]) ≥ E[φ(X)]. Egalitatea are loc NUMAI dacă φ este liniară SAU dacă X este constant (varianță zero). Greșeală frecventă în modelare ('Flaw of Averages'): inserarea valorii medii a inputului într-o funcție neliniară NU produce valoarea medie a outputului — Jensen garantează că va produce o estimare sistematic DEVIATĂ."
    },
    {
        "id": "radacinile_unitatii",
        "descriere": r"Rădăcinile unității de ordinul n, zⁿ = 1, rădăcini complexe, poligoane regulate pe cercul unitar, formula lui De Moivre.",
        "hint": r"ATENȚIE: Ecuația zⁿ = 1 are EXACT n soluții complexe distincte: ωₖ = cos(2kπ/n) + i·sin(2kπ/n) pentru k=0,1,...,n-1. SUMA tuturor rădăcinilor unității de ordin n este ZERO (pentru n≥2). PRODUSUL tuturor rădăcinilor este (-1)^(n+1). Pe câmpuri finite de caracteristică p, dacă n este multiplu de p, formula degenerează — nu mai există n rădăcini distincte! Nu confunda cu rădăcinile lui zⁿ = a (cu a≠1), care au modul r^(1/n), nu 1."
    },
    {
        "id": "aritmetica_modulo_congruente",
        "descriere": r"Congruențe modulo n, operatorul modulo, a ≡ b (mod n), clase de echivalență, aritmetică modulară.",
        "hint": r"ATENȚIE: Există o diferență critică între congruența MATEMATICĂ (a ≡ b mod n — clasă de echivalență, infinit de reprezentanți) și operatorul INFORMATIC (a % b — returnează UN SINGUR rest). În unele limbaje de programare, a % b pentru a NEGATIV returnează un rezultat NEGATIV (ex: -7 % 3 = -1 în C/C++), violând definiția matematică care impune 0 ≤ r < n. Reversul logic este o capcană: a ≡ r (mod n) NU garantează că a%n = r computațional! La împărțire în congruențe, nu împărți direct — înmulțește cu INVERSUL MODULAR (care există NUMAI dacă GCD(a,n)=1)."
    },
    {
        "id": "factorizarea_unica_numere_prime",
        "descriere": r"Teorema Fundamentală a Aritmeticii, factorizarea unică în factori primi, descompunerea oricărui întreg n>1.",
        "hint": r"ATENȚIE: Numărul 1 NU este număr prim — includerea lui în mulțimea primelor ar distruge unicitatea factorizării (orice număr ar avea infinit de factorizări: n = 1·n = 1²·n = ...). Factorizarea este unică NUMAI în inelele cu factorizare unică (UFD). În inele mai generale (ex: Z[√-5]), unicitatea poate eșua: 6 = 2·3 = (1+√-5)(1-√-5), ambele factorizări în elemente ireductibile. Un număr prim p cu proprietatea că p|ab implică p|a SAU p|b este un element PRIM (concept diferit de ireductibil în inele generale)."
    },
    {
        "id": "teorema_wilson_primalitate",
        "descriere": r"Criteriul lui Wilson de primalitate, (p-1)! ≡ -1 (mod p), condiție necesară și suficientă pentru p prim.",
        "hint": r"ATENȚIE: Deși Teorema lui Wilson oferă un criteriu NECESAR ȘI SUFICIENT de primalitate — p este prim DACĂ ȘI NUMAI DACĂ (p-1)! ≡ -1 (mod p) — ea este complet INUTILĂ practic pentru testarea primalității numerelor mari. Calculul (p-1)! are complexitate O(p·log²p), exponențial față de numărul de cifre, depășind orice resursă computațională pentru prime criptografice (sute de biți). Se folosește EXCLUSIV în demonstrații teoretice (câmpuri Galois, inversul multiplicativ). Nu confunda cu Mica Teoremă Fermat (aᵖ⁻¹ ≡ 1 mod p), care este mai slabă dar computațional fezabilă."
    },

]
