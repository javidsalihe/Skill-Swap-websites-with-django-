document.getElementById('userForm').addEventListener('submit', function(e) {
    const logField = document.getElementById('longitude_id');
    const latField = document.getElementById('latitude_id');
    const streetName = document.getElementById('street_name');
    const districtId = document.getElementById('district_id');

    if (!(logField.value || latField.value) && (streetName.value && districtId.value)) {
        e.preventDefault();

        if (confirm("Dürfen wir Ihren aktuellen Standort erfassen, um die Adresse zu vervollständigen?")) {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {

                    document.getElementById('latitude_id').value = position.coords.latitude;
                    document.getElementById('longitude_id').value = position.coords.longitude;
                    document.getElementById('timezone_id').value = Intl.DateTimeFormat().resolvedOptions().timeZone;
                    document.getElementById('userForm').submit();
                }, function(error) {
                    alert("Standortzugriff verweigert. Das Formular wird ohne Koordinaten gespeichert.");
                    document.getElementById('userForm').submit();
                });
            } else {
                alert("Geolocation wird von diesem Browser nicht unterstützt.");
                document.getElementById('userForm').submit();
            }
        } else {
            document.getElementById('userForm').submit();
        }
    }
});