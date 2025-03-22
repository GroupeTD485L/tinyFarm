package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.Entity; // représente une date avec heure sans fuseau horaire
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import com.fasterxml.jackson.annotation.JsonManagedReference;

@Entity
@Table(name = "compte")
public class Compte{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idCompte;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name=idFerme) //le nom de l'attribut dans la table compte
    private Ferme idFerme;

    private String pseudo;
    private LocalDateTime derniereConnexion;

    public Compte(){}

    public Compte(String pseudo){
        this.pseudo = pseudo;
        idFerme = new Ferme();
        this.derniereConnexion = LocalDateTime.now(); //initialisation de la derniere connexion au moment ou l'on creer le compte
    }
}