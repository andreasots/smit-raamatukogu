function elem(name, attrs, children) {
    var e = document.createElement(name);

    Object.keys(attrs).forEach(function (attr) {
        e.setAttribute(attr, attrs[attr]);
    });

    children.forEach(function (child) {
        e.appendChild(child);
    });

    return e;
}

function deleteButton(url, label, callback) {
    var btnDelete = elem("button", {"class": "btn btn-sm btn-c"}, [document.createTextNode(label)]);
    btnDelete.addEventListener("click", function (e) {
        fetch(url, {method: "DELETE"})
            .then(function (result) {
                if (result.status != 204) {
                    return result.json();
                } else {
                    return Promise.resolve({});
                }
            })
            .then(function (res) {
                if (res.errors) {
                    res.errors.forEach(function (error) {
                        alert("Kustutamine ebaõnnestus: " + error.title + ": " + error.detail);
                    });
                } else {
                    callback();
                }
            }, function (err) {
                alert("Kustutamine ebaõnnestus: " + err);
            })
    });

    return btnDelete;
}

document.addEventListener("DOMContentLoaded", function(e) {
    fetchBooks();
    fetchReaders();
    fetchLoans();
});

document.querySelector("#kataloog button").addEventListener("click", function (e) {
    fetchBooks();
});

document.querySelector("#lugejad button").addEventListener("click", function (e) {
    fetchReaders();
});

document.querySelector("#laenutus button").addEventListener("click", function (e) {
    fetchBooks();
    fetchReaders();
    fetchLoans();
});

document.getElementById("kataloog-lisa").addEventListener("click", function (e) {
    fetch(SCRIPT_ROOT + "/api/v1/books", {
        method: "POST",
        headers: {
            "Content-Type": "application/vnd.api+json",
        },
        body: JSON.stringify({
            "data": {
                "type": "book",
                "attributes": {
                    "title": document.getElementById("kataloog-pealkiri").value,
                    "author": document.getElementById("kataloog-autor").value,
                }
            }
        })
    })
        .then(function (res) {
            return res.json();
        })
        .then(function (data) {
            if (data.errors) {
                data.errors.forEach(function (error) {
                    alert("Uue raamatu lisamine ebaõnnestus: " + error.title + ": " + error.detail);
                })
            } else {
                fetchBooks();
                document.getElementById("kataloog-pealkiri").value = "";
                document.getElementById("kataloog-autor").value = "";
            }
        }, function (err) {
            alert("Uue raamatu lisamine ebaõnnestus: " + err);
        })
});

document.getElementById("lugejad-lisa").addEventListener("click", function (e) {
    fetch(SCRIPT_ROOT + "/api/v1/users", {
        method: "POST",
        headers: {
            "Content-Type": "application/vnd.api+json",
        },
        body: JSON.stringify({
            "data": {
                "type": "user",
                "attributes": {
                    "name": document.getElementById("lugejad-nimi").value,
                }
            }
        })
    })
        .then(function (res) {
            return res.json();
        })
        .then(function (data) {
            if (data.errors) {
                data.errors.forEach(function (error) {
                    alert("Uue lugeja lisamine ebaõnnestus: " + error.title + ": " + error.detail);
                })
            } else {
                fetchReaders();
                document.getElementById("lugejad-nimi").value = "";
            }
        }, function (err) {
            alert("Uue lugeja lisamine ebaõnnestus: " + err);
        })
});

document.getElementById("laenutus-lisa").addEventListener("click", function (e) {
    fetch(SCRIPT_ROOT + "/api/v1/loans", {
        method: "POST",
        headers: {
            "Content-Type": "application/vnd.api+json",
        },
        body: JSON.stringify({
            "data": {
                "type": "loan",
                "attributes": {
                },
                "relationships": {
                    "borrower": {
                        "data": {
                            "type": "user",
                            "id": document.getElementById("laenutus-laenaja").value,
                        },
                    },
                    "book": {
                        "data": {
                            "type": "book",
                            "id": document.getElementById("laenutus-raamat").value,
                        },
                    },
                },
            },
        })
    })
        .then(function (res) {
            return res.json();
        })
        .then(function (data) {
            if (data.errors) {
                data.errors.forEach(function (error) {
                    alert("Uue laenutuse lisamine ebaõnnestus: " + error.title + ": " + error.detail);
                })
            } else {
                fetchLoans();
            }
        }, function (err) {
            alert("Uue laenutuse lisamine ebaõnnestus: " + err);
        })
});

function fetchBooks() {
    var select = document.getElementById("laenutus-raamat");
    var body = document.getElementById("table-kataloog").tBodies[0];

    while (select.firstChild) {
        select.removeChild(select.firstChild);
    }

    while (body.firstChild) {
        body.removeChild(body.firstChild);
    }

    var i = 1;

    fetch(SCRIPT_ROOT + "/api/v1/books")
    .then(function (response) {
        return response.json();
    })
    .then(function (response) {
        response.data.forEach(function (book) {
            body.appendChild(elem("tr", {}, [
                elem("td", {}, [document.createTextNode(i++)]),
                elem("td", {}, [document.createTextNode(book.attributes.title)]),
                elem("td", {}, [document.createTextNode(book.attributes.author)]),
                elem("td", {}, [deleteButton(book.links.self, "Kustuta", function() { fetchBooks(); fetchLoans(); })])
            ]));
            select.appendChild(elem("option", {"value": book.id}, [document.createTextNode(book.attributes.title)]));
        })
    })
};

function fetchReaders() {
    var select = document.getElementById("laenutus-laenaja");
    var body = document.getElementById("table-lugejad").tBodies[0];

    while (select.firstChild) {
        select.removeChild(select.firstChild);
    }

    while (body.firstChild) {
        body.removeChild(body.firstChild);
    }

    var i = 1;

    fetch(SCRIPT_ROOT + "/api/v1/users")
    .then(function (response) {
        return response.json();
    })
    .then(function (response) {
        response.data.forEach(function (user) {
            body.appendChild(elem("tr", {}, [
                elem("td", {}, [document.createTextNode(i++)]),
                elem("td", {}, [document.createTextNode(user.attributes.name)]),
                elem("td", {}, [deleteButton(user.links.self, "Kustuta", fetchReaders)]),
            ]));
            select.appendChild(elem("option", {"value": user.id}, [document.createTextNode(user.attributes.name)]));
        })
    })
}

function fetchLoans() {
    var table = document.getElementById("table-laenutus");
    var body = table.tBodies[0];

    while (body.firstChild) {
        body.removeChild(body.firstChild);
    }

    var i = 1;

    fetch(SCRIPT_ROOT + "/api/v1/loans?include=book,borrower")
    .then(function (response) {
        return response.json();
    })
    .then(function (response) {
        response.data.forEach(function (loan) {
            var borrower = response.included.find(function (elem) {
                return elem.type === loan.relationships.borrower.data.type && elem.id === loan.relationships.borrower.data.id;
            });

            var book = response.included.find(function (elem) {
                return elem.type === loan.relationships.book.data.type && elem.id === loan.relationships.book.data.id;
            });

            body.appendChild(elem("tr", {}, [
                elem("td", {}, [document.createTextNode(i++)]),
                elem("td", {}, [document.createTextNode(book.attributes.title)]),
                elem("td", {}, [document.createTextNode(borrower.attributes.name)]),
                elem("td", {}, [deleteButton(loan.links.self, "Tagasta", fetchLoans)]),
            ]));
        })
    })
}
