function corriger() {
    let score = 0;

    if (document.querySelector('input[name="q1"]:checked')?.value == "1") score++;
    if (document.querySelector('input[name="q2"]:checked')?.value == "1") score++;
    if (document.querySelector('input[name="q3"]:checked')?.value == "0") score++;
    if (document.querySelector('input[name="q4"]:checked')?.value == "2") score++;

    document.getElementById("resultat").innerText =
        " Ton score : " + score + " / 4";
}
