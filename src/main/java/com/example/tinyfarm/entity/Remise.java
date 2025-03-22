package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.Entity; // représente une date avec heure sans fuseau horaire
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToOne;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "remise")
public class Remise{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idRemise;

    @OneToOne
    @JoinColumn(name=proprietaire) //le nom de l'attribut dans la table Remise
    private Ferme idFerme;

    @ManyToOne
    @JoinColumn(name=type)
    private Produit idProduit;

    private int quantite;

    public Remise(){}

}