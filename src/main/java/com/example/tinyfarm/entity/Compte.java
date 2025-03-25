package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "compte")
@Data
public class Compte{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idCompte;

    @OneToOne(cascade = CascadeType.ALL)
    @JoinColumn(name="idFerme", nullable = false) //le nom de l'attribut dans la table compte
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