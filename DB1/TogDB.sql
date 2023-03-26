
-- Opprett tabellen for Jernbanestasjon
CREATE TABLE Jernbanestasjon (
    Navn VARCHAR(50) PRIMARY KEY,
    Moh INT
);

-- Opprett tabellen for StartStasjon
CREATE TABLE StartStasjon (
    Navn VARCHAR(50) PRIMARY KEY,
    Moh INT
);

-- Opprett tabellen for  EndeStasjon
CREATE TABLE EndeStasjon (
    Navn VARCHAR(50) PRIMARY KEY,
    Moh INT
);

-- Opprett tabellen for Banestrekning
CREATE TABLE Banestrekning (
    Banenavn VARCHAR(50) PRIMARY KEY,
    Fremdriftsenergi VARCHAR(50),
    Hovedretning VARCHAR(50)
);

-- Opprett tabellen for Delstrekning
CREATE TABLE Delstrekning (
    StrekningsID INT PRIMARY KEY,
    Lengde INT CHECK (Lengde > 0) NOT NULL,
    TypeSpor VARCHAR(50),
    StartStasjonNavn VARCHAR(50) NOT NULL,
    EndeStasjonNavn VARCHAR(50) NOT NULL,
    FOREIGN KEY (StartStasjonNavn) REFERENCES StartStasjon(Navn),
    FOREIGN KEY (EndeStasjonNavn) REFERENCES EndeStasjon(Navn)
);

-- Opprett tabellen for DelbanerPåBane
CREATE TABLE DelbanerPåBane (
    StrekningsID INT,
    Banenavn VARCHAR(50),
    PRIMARY KEY (StrekningsID, Banenavn),
    FOREIGN KEY (StrekningsID) REFERENCES Delstrekning(StrekningsID),
    FOREIGN KEY (Banenavn) REFERENCES Banestrekning(Banenavn)
);

-- Opprett tabellen for Operatør
CREATE TABLE Operatør (
    OperatørID INT PRIMARY KEY,
    Navn VARCHAR(50) NOT NULL
);

-- Opprett tabellen for TogRute
CREATE TABLE TogRute (
    RuteID INT PRIMARY KEY,
    Retning VARCHAR(50),
    OperatørID INT NOT NULL,
    FOREIGN KEY (OperatørID) REFERENCES Operatør(OperatørID)
);

-- Opprett tabellen for TogRuteForekomst
CREATE TABLE TogRuteForekomst (
    RuteID INT,
    ForekomstID INT,
    Dato DATE,
    PRIMARY KEY (RuteID, ForekomstID),
    FOREIGN KEY (RuteID) REFERENCES TogRute(RuteID)
);

-- Opprett tabellen for  TogRuteTabell
CREATE TABLE TogRuteTabell (
    RuteID INT,
    TabellID INT,
    PRIMARY KEY (RuteID, TabellID),
    FOREIGN KEY (RuteID) REFERENCES TogRute(RuteID)
);

-- Opprett tabellen for Ukedag
CREATE TABLE Ukedag (
    Dag VARCHAR(50) PRIMARY KEY
);

-- Opprett tabellen for Vognoppsett
CREATE TABLE Vognoppsett (
    OppsettID INT PRIMARY KEY
);

-- Opprett tabellen for SoveVogn
CREATE TABLE SoveVogn (
    VognID INT PRIMARY KEY,
    VognType VARCHAR(50),
    FOREIGN KEY (VognID) REFERENCES VognType(VognID)
);

-- Opprett tabellen for SitteVogn
CREATE TABLE SitteVogn (
    VognID INT PRIMARY KEY,
    VognType VARCHAR(50),
    FOREIGN KEY (VognID) REFERENCES VognType(VognID)
);

-- Opprett tabellen for Sitteplas
CREATE TABLE Sitteplass (
    VognID INT,
    SitteplassNummer INT,
    VognType VARCHAR(50),
    RadStørrelse INT CHECK (RadStørrelse > 0) NOT NULL,
    PRIMARY KEY (VognID, SitteplassNummer),
    FOREIGN KEY (VognID) REFERENCES VognType(VognID)
);

-- Opprett tabellen for Soveplass
CREATE TABLE Soveplass (
    VognID INT,
    SoveplassNummer INT,
    PRIMARY KEY (VognID, SoveplassNummer),
    FOREIGN KEY (VognID) REFERENCES VognType(VognID)
);

-- Opprett tabellen for Bilett
CREATE TABLE Billett (
    BillettID INT PRIMARY KEY,
    ForekomstID INT NOT NULL,
    StartStasjonNavn VARCHAR(50) NOT NULL,
    EndeStasjonNavn VARCHAR(50) NOT NULL,
    FOREIGN KEY (ForekomstID) REFERENCES Forekomst (ForekomstID),
    FOREIGN KEY (StartStasjonNavn) REFERENCES StartStasjon (Navn),
    FOREIGN KEY (EndeStasjonNavn) REFERENCES EndeStasjon (Navn)
);

-- Opprett tabellen for Kundeordre
CREATE TABLE Kundeordre (
    Ordrenummer INT PRIMARY KEY,
    Kjøpsdato DATE,
    Kundenummer INT NOT NULL,
    FOREIGN KEY (Kundenummer) REFERENCES Kunde (Kundenummer)
);

-- Opprett tabellen for Kunde
CREATE TABLE Kunde (
    Kundenummer INT PRIMARY KEY,
    Fornavn VARCHAR(50),
    Etternavn VARCHAR(50),
    Telefon VARCHAR(20),
    Epost VARCHAR(50)
);
