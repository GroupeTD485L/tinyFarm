package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "remise")
@Data
public class Remise{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-incrémentation de l'ID
    private Long idRemise;

    @OneToOne
    @JoinColumn(name="proprietaire", nullable = false) //le nom de l'attribut dans la table Remise
    @JsonBackReference
    private Ferme proprietaire;

    @ManyToOne
    @JoinColumn(name="type", nullable = false)
    private Produit idProduit;

    private int quantite;

    public Remise(){}

    public Remise(Ferme proprietaire, Produit idProduit, int quantite) {
        this.proprietaire = proprietaire;
        this.idProduit = idProduit;
        this.quantite = quantite;
    }

}