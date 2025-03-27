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

    @Column(unique = true, nullable = false)
    private String pseudo;
    
    private LocalDateTime derniereConnexion;

    public Compte(){}

    public Compte(String pseudo, Ferme ferme){
        this.pseudo = pseudo;
        idFerme = ferme;
        this.derniereConnexion = LocalDateTime.now(); //initialisation de la derniere connexion au moment ou l'on creer le compte
    }
}