import streamlit as st
import pandas as pd
import gspread

def ucitaj_podatke():
    podaci_racuna = dict(st.secrets["gcp_service_account"])
    klijent = gspread.service_account_from_dict(podaci_racuna)

    tablica = klijent.opet("FILMOVI")
    radni_list = tablica.worksheet("filmovi")

    podaci = radni_list.get_all_records()
    filmovi = pd.DataFrame(podaci)
    
    return filmovi, radni_list

filmovi, radni_list = ucitaj_podatke()

if not filmovi.empty:
    filmovi["Godina"] = pd.to.numeric(filmovi["Godina"], errors="coerce")
    filmovi["Ocjena"] = pd.to.numeric(filmovi["Ocjena"], errors="coerce")

st.title("Moji Omiljeni filmovi")
st.subheader("Trenutni popis filmova")

if filmovi.empty:
    st.info("U tablici još nema filmova.")
else:
    st.dataframe(filmovi, hide_index=True)

st.subheader("Dodaj novi film")

with st.form("forma_za_dodavanje_filma, clear_on_submit=True"):
    naslov = st.text_input("Naslov:")
    godina = st.number_input("Godina:", min_value=1900, max_value=2026,
                             value=None, placeholder="Unesite godinu")
    zanr = st.text_input("Žanr:")
    ocjena = st.slider("Ocjena:", min_value=1, max_value=10, value=5)

    gumb_dodaj = st.form_submit_button("DODAJ FILM")

if gumb_dodaj:
    if naslov.strip() and zanr.strip() and godina is not None:
        novi_red = [naslov.strip(), int(godina), zanr.strip(), ocjena]

        radni_list.append_row(novi_red)

        st.success("Film je uspješno dodan!")
    else:
        st.warning(Unesite naslov, godinu i žanr filma.)


st.subheader("Pretraži filmove")

if filmovi.empty:
    st.info("Nema filmova za pretraživanje")

else:
    trazeni_zanr = st.text_input("Upišite žanr:")
    trazena_godina = st.number_input("Upišite godinu:", min_value 1900, max_value=2026, value=None)

    filtrirani_filmovi = filmovi

    if trazeni_zanr.strip():
        filtrirani_filmovi = filtrirani_filmovi[filtrirani_filmovi["Žanr"]
                                                .str.contains(trazeni_zanr.strip(), case = False)]

    if trazena_godina is not None:
        filtrirani_filmovi = filtrirani_filmovi[filtrirani_filmovi["Godina"] == int(trazena_godina)]

    if filtrirani_filmovi.empty:
        st.info("Nije pronađen nijedan film.")

    else:
        st.dataframe(filtrirani_filmovi, hide_index=True)


st.subheader("Brisanje filmova")

if filmovi.empty:
    st.info("Nema filmova za brisanje")
else:
    def opis_filma(indeks):
        film = filmovi.iloc[indeks]

        return(f"{film["Naslov"]} {int(film["Godina"])} {film["Žanr"]} {film["Ocjena"]}")
    
    odabrani_indeks = st.selectbox("Odaberite tekst za brisanje",
                                    options=range(len(filmovi))
                                    index=None,
                                    placeholder="Odaberite jedan film",
                                    format_func=opis_filma
                                    )
    
    if st.button("IZBRIŠI FILM"):
        if odabrani_indeks is not None:
            redak_u_tablici = odabrani_index + 2
            radni_list.delete_rows(redak_u_tablici)

            st.rerun()

        else:
            st.warning("Odaberite film za brisanje")

st.subheader("Najbolja 3 filma")

if filmovi.empty:
    st..info("Nema filmova za prikaz")

else:
    najbolja_tri = filmovi.sort_values(by="Ocjena", ascending=False).head(3)

    st.dataframe(najbolja_tri, hide_index=True)










             