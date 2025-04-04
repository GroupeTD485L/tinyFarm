package com.example.tinyfarm.entity;
import java.time.LocalDateTime;


import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "commerce")
@Data
public class Commerce{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long idTransac;

    @ManyToOne
    @JoinColumn(name = "idAcheteur", nullable = false)  // Clé étrangère vers la ferme pour acheteur
    @JsonBackReference
    private Ferme acheteur;

    @ManyToOne
    @JoinColumn(name = "idVendeur", nullable = false)  // Clé étrangère vers la ferme pour vendeur
    @JsonBackReference
    private Ferme vendeur;

    @ManyToOne
    @JoinColumn(name = "produit", nullable = false)  // Clé étrangère vers le produit
    private Produit produit;

    private int quantite;
    private float prixUnitaire;
	private LocalDateTime dateAchat;

    public Commerce(){
    }
    
    public Commerce(Ferme acheteur, Ferme vendeur, Produit produit, int quantite, float prixUnitaire) {
        this.acheteur = acheteur;
        this.vendeur = vendeur;
        this.produit = produit;
        this.quantite= quantite;
        this.prixUnitaire = prixUnitaire;
        this.dateAchat=LocalDateTime.now();
    }
}
