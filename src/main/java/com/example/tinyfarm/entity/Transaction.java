package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "transaction")
public class Transaction{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long idTransac;

    @ManyToOne
    @JoinColumn(name = "idAcheteur", nullable = false)  // Clé étrangère vers la ferme pour acheteur
    private Ferme acheteur;

    @ManyToOne
    @JoinColumn(name = "idVendeur", nullable = false)  // Clé étrangère vers la ferme pour vendeur
    private Ferme vendeur;

    @ManyToOne
    @JoinColumn(name = "produit", nullable = false)  // Clé étrangère vers le produit
    private Produit produit;

    private int quantite;
    private float prixUnitaire;
	private LocalDateTime dateAchat;

    public Transaction(int quantite,float prixUnitaire) {
        this.quantite= quantite;
        this.prixUnitaire = prixUnitaire;
        this.dateAchat=LocalDateTime.now();
    }
}
