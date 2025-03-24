package com.example.tinyfarm.entity;
import java.time.LocalDateTime;

import jakarta.persistence.*;
import lombok.Data;


@Entity
@Table(name = "produit")
public class Produit{
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long idProduit;
    
    private String nom; 
    private String description; 
    private boolean estVendable;

    public Produit(){
    }

    public Produit(String nom,String description,boolean estVendable){
        this.nom = nom;
        this.description = description;
        this.estVendable = estVendable;
    }
}
