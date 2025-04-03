package com.example.tinyfarm.entity;

import com.fasterxml.jackson.annotation.JsonBackReference;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "classement")
@Data
public class Classement{
    @Id
    private Long idClassement;

    @OneToOne
    @MapsId
    @JoinColumn(name="idFerme", nullable = false)
    @JsonBackReference
    private Ferme ferme;

    private float score;

    public Classement(){}

    public Classement(float score){
        this.score = score;
    }
}
